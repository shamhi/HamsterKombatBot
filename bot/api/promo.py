from typing import Any

import aiohttp

from bot.api.http import make_request


async def get_promos(
        http_client: aiohttp.ClientSession
) -> tuple[dict[Any, Any], dict[Any, Any]]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/get-promos',
        {},
        'getting Promos'
    )

    promos = response_json.get('promos', [])

    return promos


async def apply_promo(
        http_client: aiohttp.ClientSession, promo_code: str
) -> dict[Any, Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/apply-promo',
        {'promoCode': promo_code},
        'Apply Promo',
        ignore_status=422
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return profile_data
