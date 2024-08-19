from pyrogram import Client

from bot.config import settings
from bot.utils import logger
from bot.utils.json_db import JsonDB
from bot.utils.proxy import get_proxy_dict
from bot.utils.default import DEFAULT_HEADERS, DEFAULT_FINGERPRINT


async def register_sessions():
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.\n\n"
                         "1. Go to https://my.telegram.org and log in using your phone number.\n"
                         "2. Select \"API development tools\" and fill out the form to register a new application.\n"
                         "3. Note down the API_ID and API_HASH in .env file provided after registering your application.")

    session_name = input('\nEnter the session name (Press Enter to exit): ')

    if not session_name:
        return None

    proxy = input('\nEnter proxy (Press Enter to continue): ')

    proxy_dict = get_proxy_dict(proxy)

    session = Client(
        name=session_name,
        api_id=API_ID,
        api_hash=API_HASH,
        workdir="sessions/",
        proxy=proxy_dict,
    )

    async with session:
        user_data = await session.get_me()

    logger.success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')

    db = JsonDB("profiles")

    data = db.get_data()

    data[session_name] = {
        "proxy": proxy,
        "headers": DEFAULT_HEADERS,
        "fingerprint": DEFAULT_FINGERPRINT,
    }

    db.save_data(data)
