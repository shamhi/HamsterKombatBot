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


async def check_task(
        http_client: aiohttp.ClientSession, task_id: str
) -> tuple[dict[Any, Any], dict[Any, Any]]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/check-task',
        {'taskId': task_id},
        'Check Task',
        ignore_status=422
    )

    task = response_json.get('task', {}) or response_json.get('found', {}).get('task')
    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return task, profile_data
