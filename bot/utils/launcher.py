import sys
import asyncio
import argparse
from itertools import cycle

from pyrogram import Client

from bot.config import settings
from bot.utils import logger
from bot.utils.proxy import get_proxy_string
from bot.utils.scripts import get_session_names
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions


banner = """

▒█ ▒█ █▀▀█ █▀▄▀█ █▀▀ ▀▀█▀▀ █▀▀ █▀▀█ ▒█ ▄▀ █▀▀█ █▀▄▀█ █▀▀▄ █▀▀█ ▀▀█▀▀ ▒█▀▀█ █▀▀█ ▀▀█▀▀ 
▒█▀▀█ █▄▄█ █ ▀ █ ▀▀█   █   █▀▀ █▄▄▀ ▒█▀▄  █  █ █ ▀ █ █▀▀▄ █▄▄█   █   ▒█▀▀▄ █  █   █   
▒█ ▒█ ▀  ▀ ▀   ▀ ▀▀▀   ▀   ▀▀▀ ▀ ▀▀ ▒█ ▒█ ▀▀▀▀ ▀   ▀ ▀▀▀  ▀  ▀   ▀   ▒█▄▄█ ▀▀▀▀   ▀  

"""

async def get_tg_clients() -> list[Client]:
    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    if not settings.API_ID or not settings.API_HASH:
        print('1. Go to https://my.telegram.org and log in using your phone number.')
        print('2. Select "API development tools" and fill out the form to register a new application.')
        print('3. Note down the API_ID and API_HASH in .env file provided after registering your application.')
        sys.exit()

    tg_clients = [Client(
        name=session_name,
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        workdir='sessions/',
    ) for session_name in session_names]

    return tg_clients


async def process() -> None:
    print(banner)

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true', help='Add new session')
    args = parser.parse_args()

    session_names = get_session_names()
    logger.info(f"Detected {len(session_names)} sessions")

    if not session_names or args.add:
        await register_sessions()
    else:
        print('')

    tg_clients = await get_tg_clients()

    await run_tasks(tg_clients=tg_clients)


async def run_tasks(tg_clients: list[Client]):
    tasks = [asyncio.create_task(run_tapper(tg_client=tg_client, proxy=get_proxy_string(tg_client.name)))
             for tg_client in tg_clients]

    await asyncio.gather(*tasks)
