import json
import heapq
import asyncio
from time import time
from random import randint
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.utils import logger
from bot.utils.fingerprint import FINGERPRINT
from bot.utils.scripts import escape_html
from bot.exceptions import InvalidSession
from .headers import headers


class Tapper:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            dialogs = self.tg_client.get_dialogs()
            async for dialog in dialogs:
                if dialog.chat and dialog.chat.username and dialog.chat.username == 'hamster_kombat_bot':
                    break

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('hamster_kombat_bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    fls *= 2
                    logger.info(f"{self.session_name} | Sleep {fls}s")

                    await asyncio.sleep(fls)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                url='https://hamsterkombat.io/'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: aiohttp.ClientSession, tg_web_data: str) -> str:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/auth/auth-by-telegram-webapp',
                                              json={"initDataRaw": tg_web_data, "fingerprint": FINGERPRINT})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            access_token = response_json['authToken']

            return access_token
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def get_me_telegram(self, http_client: aiohttp.ClientSession) -> dict[str]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/auth/me-telegram',
                                              json={})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            tasks = response_json['telegramUser']

            return tasks
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Me Telegram: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def get_profile_data(self, http_client: aiohttp.ClientSession) -> dict[str]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/sync',
                                              json={})
            response_text = await response.text()
            if response.status != 422:
                response.raise_for_status()

            response_json = json.loads(response_text)
            profile_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

            return profile_data
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Profile Data: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def get_config(self, http_client: aiohttp.ClientSession) -> dict[str]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/config',
                                              json={})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            config = response_json['clickerConfig']

            return config
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Config: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def get_tasks(self, http_client: aiohttp.ClientSession) -> dict[str]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/list-tasks',
                                              json={})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            tasks = response_json['tasks']

            return tasks
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Tasks: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def select_exchange(self, http_client: aiohttp.ClientSession, exchange_id: str) -> bool:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/select-exchange',
                                              json={'exchangeId': exchange_id})
            response_text = await response.text()
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Select Exchange: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

            return False

    async def get_daily(self, http_client: aiohttp.ClientSession):
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/check-task',
                                              json={'taskId': "streak_days"})
            response_text = await response.text()
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Daily: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

            return False

    async def apply_boost(self, http_client: aiohttp.ClientSession, boost_id: str) -> bool:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/buy-boost',
                                              json={'timestamp': time(), 'boostId': boost_id})
            response_text = await response.text()
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Apply {boost_id} Boost: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

            return False

    async def get_upgrades(self, http_client: aiohttp.ClientSession) -> list[dict]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/upgrades-for-buy',
                                              json={})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            upgrades = response_json['upgradesForBuy']

            return upgrades
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Upgrades: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def buy_upgrade(self, http_client: aiohttp.ClientSession, upgrade_id: str) -> tuple[bool, dict[str]]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/buy-upgrade',
                                              json={'timestamp': time(), 'upgradeId': upgrade_id})
            response_text = await response.text()
            if response.status != 422:
                response.raise_for_status()

            response_json = json.loads(response_text)
            upgrades = response_json.get('upgradesForBuy') or response_json.get('found', {}).get('upgradesForBuy', {})

            return True, upgrades
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while buying Upgrade: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

            return False, {}

    async def get_boosts(self, http_client: aiohttp.ClientSession) -> list[dict]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/boosts-for-buy', json={})
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            boosts = response_json['boostsForBuy']

            return boosts
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Boosts: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def send_taps(self, http_client: aiohttp.ClientSession, available_energy: int, taps: int) -> dict[str]:
        response_text = ''
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/tap',
                                              json={'availableTaps': available_energy, 'count': taps,
                                                    'timestamp': time()})
            response_text = await response.text()
            if response.status != 422:
                response.raise_for_status()

            response_json = json.loads(response_text)
            player_data = response_json.get('clickerUser') or response_json.get('found', {}).get('clickerUser', {})

            return player_data
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Tapping: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        turbo_time = 0
        active_turbo = False

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)

        if proxy:
            await self.check_proxy(http_client=http_client, proxy=proxy)

        tg_web_data = await self.get_tg_web_data(proxy=proxy)

        while True:
            try:
                if time() - access_token_created_time >= 3600:
                    access_token = await self.login(http_client=http_client, tg_web_data=tg_web_data)

                    if not access_token:
                        continue

                    http_client.headers["Authorization"] = f"Bearer {access_token}"

                    access_token_created_time = time()

                    await self.get_me_telegram(http_client=http_client)
                    await self.get_config(http_client=http_client)

                    profile_data = await self.get_profile_data(http_client=http_client)

                    if not profile_data:
                        continue

                    last_passive_earn = profile_data['lastPassiveEarn']
                    earn_on_hour = profile_data['earnPassivePerHour']

                    logger.info(f"{self.session_name} | Last passive earn: <g>+{last_passive_earn:,}</g> | "
                                f"Earn every hour: <y>{earn_on_hour:,}</y>")

                    available_energy = profile_data.get('availableTaps', 0)
                    balance = int(profile_data.get('balanceCoins', 0))

                    upgrades = await self.get_upgrades(http_client=http_client)
                    boosts = await self.get_boosts(http_client=http_client)
                    tasks = await self.get_tasks(http_client=http_client)

                    daily_task = tasks[-1]
                    rewards = daily_task['rewardsByDays']
                    is_completed = daily_task['isCompleted']
                    days = daily_task['days']

                    await asyncio.sleep(delay=2)

                    if is_completed is False:
                        status = await self.get_daily(http_client=http_client)
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully get daily reward | "
                                           f"Days: <m>{days}</m> | Reward coins: {rewards[days - 1]['rewardCoins']}")

                    await asyncio.sleep(delay=2)

                    exchange_id = profile_data.get('exchangeId')
                    if not exchange_id:
                        status = await self.select_exchange(http_client=http_client, exchange_id="bybit")
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully selected exchange <y>Bybit</y>")

                taps = randint(a=settings.RANDOM_TAPS_COUNT[0], b=settings.RANDOM_TAPS_COUNT[1])

                if active_turbo:
                    taps += settings.ADD_TAPS_ON_TURBO
                    if time() - turbo_time > 20:
                        active_turbo = False
                        turbo_time = 0

                player_data = await self.send_taps(http_client=http_client,
                                                   available_energy=available_energy,
                                                   taps=taps)

                if not player_data:
                    continue

                available_energy = player_data.get('availableTaps', 0)
                new_balance = int(player_data.get('balanceCoins', 0))
                calc_taps = new_balance - balance
                balance = new_balance
                total = int(player_data.get('totalCoins', 0))
                earn_on_hour = player_data['earnPassivePerHour']

                energy_boost = next((boost for boost in boosts if boost['id'] == 'BoostFullAvailableTaps'), {})

                logger.success(f"{self.session_name} | Successful tapped! | "
                               f"Balance: <c>{balance:,}</c> (<g>+{calc_taps:,}</g>) | Total: <e>{total:,}</e>")

                if active_turbo is False:
                    if (settings.APPLY_DAILY_ENERGY is True
                            and available_energy < settings.MIN_AVAILABLE_ENERGY
                            and energy_boost.get("cooldownSeconds", 0) == 0
                            and energy_boost.get("level", 0) <= energy_boost.get("maxLevel", 0)):
                        logger.info(f"{self.session_name} | Sleep 5s before apply energy boost")
                        await asyncio.sleep(delay=5)

                        status = await self.apply_boost(http_client=http_client, boost_id="BoostFullAvailableTaps")
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully apply energy boost")

                            await asyncio.sleep(delay=1)

                            continue

                    if settings.AUTO_UPGRADE is True:
                        for _ in range(settings.UPGRADES_COUNT):
                            available_upgrades = [
                                data for data in upgrades
                                if data['isAvailable'] is True
                                   and data['isExpired'] is False
                                   and data.get('cooldownSeconds', 0) == 0
                                   and data.get('maxLevel', data['level']) >= data['level']
                                   and (data.get('condition') is None
                                        or data['condition'].get('_type') != 'SubscribeTelegramChannel')
                            ]

                            queue = []

                            for upgrade in available_upgrades:
                                upgrade_id = upgrade['id']
                                level = upgrade['level']
                                price = upgrade['price']
                                profit = upgrade['profitPerHourDelta']

                                significance = profit / max(price, 1)

                                free_money = balance - settings.BALANCE_TO_SAVE
                                max_price_limit = earn_on_hour * 5

                                if ((free_money * 0.7) >= price
                                        and level <= settings.MAX_LEVEL
                                        and profit > 0
                                        and price < max_price_limit):
                                    heapq.heappush(queue, (-significance, upgrade_id, upgrade))

                            if not queue:
                                continue

                            top_card = heapq.nsmallest(1, queue)[0]

                            upgrade = top_card[2]

                            upgrade_id = upgrade['id']
                            level = upgrade['level']
                            price = upgrade['price']
                            profit = upgrade['profitPerHourDelta']

                            logger.info(f"{self.session_name} | Sleep 5s before upgrade <e>{upgrade_id}</e>")
                            await asyncio.sleep(delay=5)

                            status, upgrades = await self.buy_upgrade(http_client=http_client,
                                                                      upgrade_id=upgrade_id)

                            if status is True:
                                earn_on_hour += profit
                                balance -= price
                                logger.success(
                                    f"{self.session_name} | "
                                    f"Successfully upgraded <e>{upgrade_id}</e> with price <r>{price:,}</r> to <m>{level}</m> lvl | "
                                    f"Earn every hour: <y>{earn_on_hour:,}</y> (<g>+{profit:,}</g>) | "
                                    f"Money left: <e>{balance:,}</e>")

                                await asyncio.sleep(delay=1)

                                continue

                    if available_energy < settings.MIN_AVAILABLE_ENERGY:
                        await http_client.close()
                        if proxy_conn:
                            proxy_conn.close()

                        random_sleep = randint(settings.SLEEP_BY_MIN_ENERGY[0], settings.SLEEP_BY_MIN_ENERGY[1])

                        logger.info(f"{self.session_name} | Minimum energy reached: {available_energy}")
                        logger.info(f"{self.session_name} | Sleep {random_sleep:,}s")

                        await asyncio.sleep(delay=random_sleep)

                        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None
                        http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)

                        access_token_created_time = 0

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)

            else:
                sleep_between_clicks = randint(a=settings.SLEEP_BETWEEN_TAP[0], b=settings.SLEEP_BETWEEN_TAP[1])

                if active_turbo is True:
                    sleep_between_clicks = 4

                logger.info(f"Sleep {sleep_between_clicks}s")
                await asyncio.sleep(delay=sleep_between_clicks)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
