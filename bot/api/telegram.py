import aiohttp
from typing import Any, Dict

from bot.api.http import make_post_request


async def get_me_telegram(
    http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_post_request(
        http_client,
        'https://api.hamsterkombat.io/auth/me-telegram',
        {},
        'getting Me Telegram',
    )
    tasks = response_json.get('telegramUser')
    return tasks
