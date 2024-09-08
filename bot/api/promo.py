
from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

from bot.api.http import make_request


async def get_apps_info(
        http_client: aiohttp.ClientSession,
) -> List[Dict[str, Any]]:
    response_json = await make_request(
        http_client,
        'GET',
        'https://api21.datavibe.top/api/Games',
        {},
        'getting Apps Info'
    )

    return response_json


async def get_promos(
        http_client: aiohttp.ClientSession
) -> Dict[str, Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/get-promos',
        {},
        'getting Promos'
    )

    return response_json


async def apply_promo(
        http_client: aiohttp.ClientSession, promo_code: str
) -> Tuple[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/apply-promo',
        {'promoCode': promo_code},
        'Apply Promo',
        ignore_status=422
    )

    profile_data = response_json.get('clickerUser', {}) or response_json.get('found', {}).get('clickerUser', {})
    promo_state = response_json.get('promoState', {}) or response_json.get('found', {}).get('promoState', {})
    reward_promo = response_json.get('reward', {}) or response_json.get('found', {}).get('reward', {})

    return profile_data, promo_state, reward_promo
