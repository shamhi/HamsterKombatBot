from typing import Any

import aiohttp

from bot.api.http import make_request


async def get_tasks(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/list-tasks',
        {},
        'getting Tasks',
    )
    tasks = response_json.get('tasks')
    return tasks


async def get_airdrop_tasks(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/list-airdrop-tasks',
        {},
        'getting Airdrop Tasks',
    )
    tasks = response_json.get('tasks')
    return tasks


async def claim_daily_reward(
        http_client: aiohttp.ClientSession
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/check-task',
        {'taskId': 'streak_days'},
        'getting Daily',
    )
    return bool(response_json)
