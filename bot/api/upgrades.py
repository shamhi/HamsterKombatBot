from time import time
from typing import Any

import aiohttp

from bot.api.http import make_request


async def get_upgrades(
        http_client: aiohttp.ClientSession
) -> dict:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/upgrades-for-buy',
        {},
        'getting Upgrades',
    )

    return response_json


async def buy_upgrade(
        http_client: aiohttp.ClientSession, upgrade_id: str
) -> tuple[bool, Any] | tuple[bool, None]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/buy-upgrade',
        {'timestamp': int(time()), 'upgradeId': upgrade_id},
        'buying Upgrade',
        ignore_status=422,
    )

    upgrades = response_json.get('upgradesForBuy') or response_json.get('found', {}).get('upgradesForBuy', {})

    return True, upgrades
