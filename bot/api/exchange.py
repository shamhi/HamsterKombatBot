import aiohttp

from bot.api.http import make_request


async def select_exchange(
        http_client: aiohttp.ClientSession, exchange_id: str
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/select-exchange',
        {'exchangeId': exchange_id},
        'Select Exchange',
    )
    return bool(response_json)
