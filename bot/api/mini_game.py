from typing import Any

import aiohttp

from bot.api.http import make_request


async def start_daily_mini_game(
        http_client: aiohttp.ClientSession
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/start-keys-minigame',
        {},
        'Start Mini Game',
    )
    return response_json


async def claim_daily_mini_game(
        http_client: aiohttp.ClientSession, cipher: str
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame',
        {'cipher': cipher},
        'Claim Mini Game',
    )
    return response_json
