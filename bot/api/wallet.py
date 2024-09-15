from typing import Any, Union, Dict, List, Optional, Tuple

import aiohttp

from bot.api.http import make_request


async def set_ton_wallet(
        http_client: aiohttp.ClientSession, address: str
) -> Dict[str, Any]:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/withdraw/set-wallet-as-default',
        {
            "id": "TonWallet",
            "walletAddress": address
        },
        'Set Ton Wallet',
        422
    )

    profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

    return profile_data
