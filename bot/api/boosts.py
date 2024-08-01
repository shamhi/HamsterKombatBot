from time import time

import aiohttp

from bot.api.http import make_request


async def get_boosts(
        http_client: aiohttp.ClientSession
) -> list[dict]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/boosts-for-buy',
        {},
        'getting Boosts',
    )

    boosts = response_json.get('boostsForBuy', [])

    return boosts


async def apply_boost(
        http_client: aiohttp.ClientSession, boost_id: str
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/buy-boost',
        {'timestamp': int(time()), 'boostId': boost_id},
        'Apply Boost',
    )

    return bool(response_json)
