import json
import asyncio

import aiohttp

from bot.utils.logger import logger
from bot.utils.scripts import escape_html


async def make_request(
        http_client: aiohttp.ClientSession,
        method: str,
        url: str,
        json_data: dict,
        error_context: str,
        ignore_status: int | None = None,
) -> dict:
    response_text = ''
    try:
        response = await http_client.request(method=method, url=url, json=json_data)
        response_text = await response.text()
        if ignore_status is None or response.status != ignore_status:
            response.raise_for_status()
        response_json = json.loads(response_text)
        return response_json
    except Exception as error:
        await handle_error(error, response_text, error_context)
        return {}


async def handle_error(error: Exception, response_text: str, context: str):
    logger.error(
        f'Unknown error while {context}: {error} | '
        f'Response text: {escape_html(response_text)[:256]}...'
    )
    await asyncio.sleep(delay=3)
