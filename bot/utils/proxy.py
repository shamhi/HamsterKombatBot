import aiohttp
from better_proxy import Proxy

from bot.utils.logger import logger
from bot.utils.json_db import JsonDB


def get_proxy_dict(proxy: str):
    try:
        proxy = Proxy.from_str(proxy=proxy.strip())

        proxy_dict = dict(
            scheme=proxy.protocol,
            hostname=proxy.host,
            port=proxy.port,
            username=proxy.login,
            password=proxy.password,
        )

        return proxy_dict
    except ValueError:
        return None


def get_proxy_string(name: str):
    db = JsonDB("sessions/profiles")

    data = db.get_data()
    proxy = data.get(name, {}).get("proxy", "")

    return proxy


async def check_proxy(
        http_client: aiohttp.ClientSession, proxy: str, session_name: str
) -> None:
    try:
        response = await http_client.get(url='https://ipinfo.io/json', timeout=aiohttp.ClientTimeout(5))
        response.raise_for_status()

        response_json = await response.json()
        ip = response_json.get('ip', 'NO')

        logger.info(f'{session_name} | Proxy IP: <lw>{ip}</lw>')
    except Exception as error:
        logger.error(f'{session_name} | Proxy: <le>{proxy}</le> | Error: <lr>{error}</lr>')
