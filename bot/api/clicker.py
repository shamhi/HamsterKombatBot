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
        profile_data = response_json.get('clickerUser') or response_json.get(
            'found', {}
        ).get('clickerUser', {})
        if profile_data:
            return profile_data


async def get_upgrades(http_client: aiohttp.ClientSession) -> dict:
    return await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy',
        {},
        'getting Upgrades',
    )


async def buy_upgrade(
        http_client: aiohttp.ClientSession, upgrade_id: str
) -> tuple[bool, Any] | tuple[bool, None]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/buy-upgrade',
        {'timestamp': time(), 'upgradeId': upgrade_id},
        'buying Upgrade',
        ignore_status=422,
    )
    upgrades = response_json.get('upgradesForBuy') or response_json.get(
        'found', {}
    ).get('upgradesForBuy', {})
    return True, upgrades


async def get_boosts(http_client: aiohttp.ClientSession) -> list[dict]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/boosts-for-buy',
        {},
        'getting Boosts',
    )
    boosts = response_json.get('boostsForBuy', [])
    return boosts


async def claim_daily_cipher(
        http_client: aiohttp.ClientSession, cipher: str
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/claim-daily-cipher',
        {'cipher': cipher},
        'Claim Daily Cipher',
    )
    return bool(response_json)


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
            'timestamp': time(),
        },
        'Tapping',
        ignore_status=422,
    )
    player_data = response_json.get('clickerUser') or response_json.get(
        'found', {}
    ).get('clickerUser', {})
    return player_data


async def apply_boost(
        http_client: aiohttp.ClientSession, boost_id: str
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/buy-boost',
        {'timestamp': time(), 'boostId': boost_id},
        'Apply Boost',
    )
    return bool(response_json)
