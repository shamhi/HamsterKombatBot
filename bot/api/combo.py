import aiohttp

from bot.api.http import make_request


async def get_combo_cards(http_client: aiohttp.ClientSession) -> dict:
    return await make_request(
        http_client,
        'POST',
        'https://api21.datavibe.top/api/GetCombo',
        {},
        'getting Combo Cards',
    )


async def claim_daily_combo(
        http_client: aiohttp.ClientSession
) -> bool:
    response_json = await make_request(
        http_client,
        'POST',
        'https://api.hamsterkombatgame.io/clicker/claim-daily-combo',
        {},
        'Claim Daily Combo',
    )
    return bool(response_json)
