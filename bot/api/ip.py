import aiohttp

from bot.api.http import make_request


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
