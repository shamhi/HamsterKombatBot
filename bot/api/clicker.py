from time import time
from typing import Any

import aiohttp

from bot.api.http import make_request


async def get_config(
        http_client: aiohttp.ClientSession,
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/config',
        {},
        'getting Config',
    )

    return response_json


async def get_profile_data(http_client: aiohttp.ClientSession) -> dict[str]:
    while True:
        response_json = await make_request(
            http_client,
            'POST',
            'https://api.hamsterkombatgame.io/clicker/sync',
            {},
            'getting Profile Data',
            ignore_status=422,
        )

        profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

        return profile_data


async def get_ip_info(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/ip',
        {},
        'getting Ip Info',
    )
    return response_json


async def get_account_info(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/auth/account-info',
        {},
        'getting Account Info',
    )
    return response_json


async def send_taps(
        http_client: aiohttp.ClientSession, available_energy: int, taps: int
) -> dict[Any, Any] | Any:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/tap',
        {
            'availableTaps': available_energy,
            'count': taps,
            'timestamp': int(time()),
        },
        'Tapping',
        ignore_status=422,
    )

    player_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return player_data
