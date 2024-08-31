from typing import Any

import aiohttp

from bot.api.http import make_request


async def start_daily_mini_game(
        http_client: aiohttp.ClientSession, mini_game_id: str
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/start-keys-minigame',
        {'miniGameId': mini_game_id},
        'Start Mini Game',
        ignore_status=422
    )

    return response_json


async def claim_daily_mini_game(
        http_client: aiohttp.ClientSession, cipher: str, mini_game_id: str
) -> tuple[dict[Any, Any], dict[Any, Any], int]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/claim-daily-keys-minigame',
        {'cipher': cipher, 'miniGameId': mini_game_id},
        'Claim Mini Game',
        ignore_status=422
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})
    daily_mini_game = response_json.get('dailyKeysMiniGames') or response_json.get('found', {}).get(
        'dailyKeysMiniGames', {})
    bonus = int(response_json.get('bonus') or response_json.get('found', {}).get('bonus', 0))

    return profile_data, daily_mini_game, bonus
