from time import time
from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

from bot.api.http import make_request


async def get_version_config(
        http_client: aiohttp.ClientSession, config_version: str
) -> Union[Dict[Any, Any], Any]:
    response_json = await make_request(
        http_client,
        'GET',
        f'https://api.hamsterkombatgame.io/clicker/config/{config_version}',
        {},
        'getting Version Config',
    )
    version_config = response_json.get('config')

    return version_config


async def get_game_config(
        http_client: aiohttp.ClientSession,
) -> Union[Dict[Any, Any], Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/config',
        {},
        'getting Game Config',
    )

    return response_json


async def get_profile_data(http_client: aiohttp.ClientSession) -> Dict[str, Any]:
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


async def get_skins(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/get-skin',
        {},
        'getting Skins',
    )
    return response_json


async def send_taps(
        http_client: aiohttp.ClientSession, available_energy: int, taps: int
) -> Union[Dict[Any, Any], Any]:
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

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return profile_data
