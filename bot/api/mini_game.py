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
        ignore_status=422
    )

    return response_json


async def claim_daily_mini_game(
        http_client: aiohttp.ClientSession, cipher: str
) -> tuple[dict[Any, Any], dict[Any, Any]]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame',
        {'cipher': cipher},
        'Claim Mini Game',
        ignore_status=422
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})
    daily_mini_game = response_json.get('dailyKeysMiniGame') or response_json.get('found', {}).get('dailyKeysMiniGame', {})

    return profile_data, daily_mini_game
