import aiohttp

from bot.utils.logger import logger


async def check_proxy(
    http_client: aiohttp.ClientSession, proxy: str, session_name: str
) -> None:
    try:
        response = await http_client.get(
            url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5)
        )
        ip = (await response.json()).get('origin')
        logger.info(f'{session_name} | Proxy IP: {ip}')
    except Exception as error:
        logger.error(f'{session_name} | Proxy: {proxy} | Error: {error}')
