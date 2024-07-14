from typing import Any

import aiohttp

from bot.api.http import handle_error, make_request


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


async def get_daily(http_client: aiohttp.ClientSession) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/check-task',
        {'taskId': 'streak_days'},
        'getting Daily',
    )
    return bool(response_json)


async def get_nuxt_builds(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any]:
    response_text = None
    try:
        response_json = await make_request(
            http_client,
            'GET',
            'https://hamsterkombatgame.io/_nuxt/builds/meta/8ec5c889-d6a0-4342-8ac7-94a4abfcf5b1.json',
            None,
            'getting Nuxt Builds'
        )
        return response_json
    except Exception as error:
        await handle_error(error, response_text, 'getting Nuxt Builds')
        return {}
