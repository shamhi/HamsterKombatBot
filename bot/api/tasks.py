
from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

from bot.api.http import make_request


async def get_tasks(
        http_client: aiohttp.ClientSession,
) -> Union[Dict[Any, Any], Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/interlude/list-tasks',
        {},
        'getting Tasks',
    )
    tasks = response_json.get('tasks', [])

    return tasks


async def get_airdrop_tasks(
        http_client: aiohttp.ClientSession,
) -> Union[Dict[Any, Any], Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/interlude/list-airdrop-tasks',
        {},
        'getting Airdrop Tasks',
    )
    tasks = response_json.get('tasks')
    return tasks


async def check_task(
        http_client: aiohttp.ClientSession, task_id: str
) -> Tuple[Dict[Any, Any], Dict[Any, Any]]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/interlude/check-task',
        {'taskId': task_id},
        'Check Task',
        ignore_status=422
    )

    task = response_json.get('task', {}) or response_json.get('found', {}).get('task')
    profile_data = response_json.get('interludeUser') or response_json.get('found', {}).get('interludeUser', {})

    return task, profile_data
