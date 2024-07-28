from typing import Any

import aiohttp

from bot.api.http import make_request, handle_error


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
