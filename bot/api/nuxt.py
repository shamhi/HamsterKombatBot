from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

from bot.api.http import make_request, handle_error


async def get_nuxt_builds(
        http_client: aiohttp.ClientSession,
) -> Dict[Any, Any]:
    response_text = None
    try:
        response_json = await make_request(
            http_client,
            'GET',
            'https://hamsterkombatgame.io/_nuxt/builds/meta/fe021024-d4a8-4ad9-ab6f-3ce2a6e9db47.json',
            None,
            'getting Nuxt Builds'
        )
        return response_json
    except Exception as error:
        await handle_error(error, response_text, 'getting Nuxt Builds')
        return {}
