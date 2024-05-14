import os
import glob
import shutil
import asyncio
import argparse

from pyrogram import Client
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions
from db.base import Base


start_text = """

▒█ ▒█ █▀▀█ █▀▄▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ ▒█ ▄▀ █▀▀█ █▀▄▀█ █▀▀▄ █▀▀█ ▀▀█▀▀ ▒█▀▀█ █▀▀█ ▀▀█▀▀ 
▒█▀▀█ █▄▄█ █ ▀ █ ▀▀█   █   █▀▀ █▄▄▀ ▒█▀▄  █  █ █ ▀ █ █▀▀▄ █▄▄█   █   ▒█▀▀▄ █  █   █   
▒█ ▒█ ▀  ▀ ▀   ▀ ▀▀▀   ▀   ▀▀▀ ▀ ▀▀ ▒█ ▒█ ▀▀▀▀ ▀   ▀ ▀▀▀  ▀  ▀   ▀   ▒█▄▄█ ▀▀▀▀   ▀  

Select an action:

    1. Create session
    2. Run clicker
"""

checked_sessions = []


def get_session_names() -> list[str]:
    session_names = glob.glob('sessions/*.session')
    session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]

    return session_names


def get_bad_session_names() -> list[str]:
    try:
        with open('sessions/bad_sessions.txt', 'r') as file:
            bad_sessions = [session_name.strip('\n').split('.session')[0] for session_name in file.readlines()]
    except FileNotFoundError:
        bad_sessions = []

    return bad_sessions


def move_bad_sessions() -> None:
    if not os.path.exists(path='sessions/bad_sessions/'):
        os.mkdir(path='sessions/bad_sessions')

    bad_session_names = get_bad_session_names()

    for session_name in bad_session_names:
        shutil.move(f'sessions/{session_name}.session', f'sessions/bad_sessions/{session_name}.session')

    with open('sessions/bad_sessions.txt', 'w') as file:
        file.write('')


async def check_sessions(session: Client) -> Client:
    is_auth = await session.connect()

    if is_auth is False:
        with open('sessions/bad_sessions.txt', 'a') as file:
            file.write(f"{session.name}.session\n")

        return

    checked_sessions.append(session)
    await session.disconnect()


async def get_tg_clients() -> list[Client]:
    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    if not settings.API_ID or not settings.API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    bad_sessions = get_bad_session_names()

    tg_clients = [Client(
        name=session_name,
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        workdir='sessions/',
        plugins=dict(root='bot/plugins')
    ) for session_name in session_names if session_name not in bad_sessions]

    check_tasks = [check_sessions(tg_client) for tg_client in tg_clients]

    await asyncio.gather(*check_tasks)
    tg_clients = checked_sessions

    return tg_clients


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action', type=int, help='Action to perform')

    move_bad_sessions()

    logger.info(f"Detected {len(get_session_names())} sessions")

    url = f'{settings.DB_ENGINE}://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
    engine = create_async_engine(url=url, echo=False, future=True)
    db_pool = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    if settings.CREATE_ALL_TABLES:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    action = parser.parse_args().action

    if not action:
        print(start_text)

        while True:
            action = input("> ")

            if not action.isdigit():
                logger.warning("Action must be number")
            elif action not in ['1', '2']:
                logger.warning("Action must be 1 or 2")
            else:
                action = int(action)
                break

    if action == 1:
        await register_sessions()
    elif action == 2:
        tg_clients = await get_tg_clients()

        await run_tasks(tg_clients=tg_clients, db_pool=db_pool)


async def run_tasks(tg_clients: list[Client], db_pool: async_sessionmaker) -> None:
    tasks = [run_tapper(tg_client=tg_client, db_pool=db_pool) for tg_client in tg_clients]
    limit = 10
    offset = 0

    while True:
        chunk = tasks[offset:offset + limit]

        if not chunk:
            tasks = [run_tapper(tg_client=tg_client, db_pool=db_pool) for tg_client in tg_clients]

            limit = 10
            offset = 0

            continue

        try:
            await asyncio.gather(*chunk)
        except Exception as error:
            logger.error(f"Top error: {error}")

        offset += limit

        await asyncio.sleep(delay=2)
