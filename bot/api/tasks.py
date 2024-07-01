import aiohttp
from typing import Any
from bot.api.http import handle_error, make_post_request


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


async def get_airdrop_tasks(
    http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_post_request(
        http_client,
        'https://api.hamsterkombat.io/clicker/list-airdrop-tasks',
        {},
        'getting Airdrop Tasks',
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


async def get_nuxt_builds(
    http_client: aiohttp.ClientSession,
) -> dict[Any, Any]:
    response_text = None
    try:
        response = await http_client.get(
            url='https://hamsterkombat.io/_nuxt/builds/meta/32ddd2fc-00f7-4814-bc32-8f160963692c.json'
        )
        response_text = await response.text()
        response.raise_for_status()
        response_json = await response.json()
        nuxt_builds = response_json
        return nuxt_builds
    except Exception as error:
        await handle_error(error, response_text, 'getting Nuxt Builds')
        return {}
