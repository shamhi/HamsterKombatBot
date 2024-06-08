import aiohttp
from typing import Any

from bot.api.http import make_post_request
from bot.utils.fingerprint import FINGERPRINT


async def login(
    http_client: aiohttp.ClientSession, tg_web_data: str
) -> Any | None:
    response_json = await make_post_request(
        http_client,
        'https://api.hamsterkombat.io/auth/auth-by-telegram-webapp',
        {'initDataRaw': tg_web_data, 'fingerprint': FINGERPRINT},
        'getting Access Token',
        # ignore_status=422
    )
    access_token = response_json.get('authToken')
    return access_token
