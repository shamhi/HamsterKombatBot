from typing import Any

import aiohttp

from bot.api.http import make_request


async def get_me_telegram(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/auth/me-telegram',
        {},
        'getting Me Telegram',
    )
    tasks = response_json.get('telegramUser')
    return tasks
