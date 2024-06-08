import aiohttp
from typing import Any, Dict
from bot.api.http import make_post_request


async def get_tasks(
    http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_post_request(
        http_client,
        'https://api.hamsterkombat.io/clicker/list-tasks',
        {},
        'getting Tasks',
    )
    tasks = response_json.get('tasks')
    return tasks


async def get_daily(http_client: aiohttp.ClientSession) -> bool:
    response_json = await make_post_request(
        http_client,
        'https://api.hamsterkombat.io/clicker/check-task',
        {'taskId': 'streak_days'},
        'getting Daily',
    )
    return bool(response_json)
