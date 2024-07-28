import aiohttp

from bot.api.http import make_request


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
