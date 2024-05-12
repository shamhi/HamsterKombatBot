import asyncio
from time import time
from random import randint
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.types import User
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.config import settings
from bot.utils import logger
from bot.exceptions import InvalidSession
from db.functions import get_user_proxy, get_user_agent, save_log
from .headers import headers


local_db = {}


class Tapper:
    def __init__(self, tg_client: Client, db_pool: async_sessionmaker, user_data: User):
        self.session_name = tg_client.name
        self.tg_client = tg_client
        self.db_pool = db_pool
        self.user_data = user_data

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

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('hamster_kombat_bot'),
                bot=await self.tg_client.resolve_peer('hamster_kombat_bot'),
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
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/auth/auth-by-telegram-webapp',
                                              json={"initDataRaw": tg_web_data, "fingerprint": {}})
            response.raise_for_status()

            response_json = await response.json()
            access_token = response_json['authToken']

            return access_token
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error}")
            await asyncio.sleep(delay=3)

    async def get_profile_data(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/sync',
                                              json={})
            response.raise_for_status()

            response_json = await response.json()
            profile_data = response_json['clickerUser']

            return profile_data
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Profile Data: {error}")
            await asyncio.sleep(delay=3)

    async def get_tasks(self, http_client: aiohttp.ClientSession) -> dict[str]:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/list-tasks',
                                              json={})
            response.raise_for_status()

            response_json = await response.json()
            tasks = response_json['tasks']

            return tasks
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Tasks: {error}")
            await asyncio.sleep(delay=3)

    async def select_exchange(self, http_client: aiohttp.ClientSession, exchange_id: str) -> bool:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/select-exchange',
                                              json={'exchangeId': exchange_id})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Select Exchange: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def get_daily(self, http_client: aiohttp.ClientSession):
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/check-task',
                                              json={'taskId': "streak_days"})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Daily: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def apply_boost(self, http_client: aiohttp.ClientSession, boost_id: str) -> bool:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/buy-boost',
                                              json={'timestamp': time(), 'boostId': boost_id})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Apply {boost_id} Boost: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def get_upgrades(self, http_client: aiohttp.ClientSession) -> list[dict]:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/upgrades-for-buy',
                                              json={})
            response.raise_for_status()

            response_json = await response.json()
            upgrades = response_json['upgradesForBuy']

            return upgrades
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Upgrades: {error}")
            await asyncio.sleep(delay=3)

    async def buy_upgrade(self, http_client: aiohttp.ClientSession, upgrade_id: str) -> bool:
        try:
            response = await http_client.post(url='https://api.hamsterkombat.io/clicker/buy-upgrade',
                                              json={'timestamp': time(), 'upgradeId': upgrade_id})
            response.raise_for_status()

            return True
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while buying Upgrade: {error}")
            await asyncio.sleep(delay=3)

            return False

    async def send_taps(self, http_client: aiohttp.ClientSession, available_energy: int, taps: int) -> dict[str]:
        try:
            response = await http_client.post(
                url='https://api.hamsterkombat.io/clicker/tap',
                json={'availableTaps': available_energy, 'count': taps, 'timestamp': time()})
            response.raise_for_status()

            response_json = await response.json()
            player_data = response_json['clickerUser']

            return player_data
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Tapping: {error}")
            await asyncio.sleep(delay=3)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        turbo_time = 0
        active_turbo = False

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        user_agent = await get_user_agent(db_pool=self.db_pool, phone_number=self.user_data.phone_number)
        headers['User-Agent'] = user_agent

        async with (aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client):
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            try:
                local_token = local_db[self.session_name]['Token']
                if not local_token:
                    tg_web_data = await self.get_tg_web_data(proxy=proxy)
                    access_token = await self.login(http_client=http_client, tg_web_data=tg_web_data)

                    http_client.headers["Authorization"] = f"Bearer {access_token}"
                    headers["Authorization"] = f"Bearer {access_token}"

                    profile_data = await self.get_profile_data(http_client=http_client)

                    exchange_id = profile_data.get('exchangeId')
                    if not exchange_id:
                        status = await self.select_exchange(http_client=http_client, exchange_id="bybit")
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully selected exchange <y>Bybit</y>")

                    last_passive_earn = profile_data['lastPassiveEarn']
                    earn_on_hour = profile_data['earnPassivePerHour']

                    logger.info(f"{self.session_name} | Last passive earn: <g>+{last_passive_earn}</g> | "
                                f"Earn every hour: <y>{earn_on_hour}</y>")

                    available_energy = profile_data.get('availableTaps', 0)
                    balance = int(profile_data['balanceCoins'])

                    local_db[self.session_name]['Balance'] = balance

                    tasks = await self.get_tasks(http_client=http_client)

                    daily_task = tasks[-1]
                    rewards = daily_task['rewardsByDays']
                    is_completed = daily_task['isCompleted']
                    days = daily_task['days']

                    if is_completed is False:
                        status = await self.get_daily(http_client=http_client)
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully get daily reward | "
                                           f"Days: <m>{days}</m> | Reward coins: {rewards[days-1]['rewardCoins']}")
                else:
                    http_client.headers["Authorization"] = f"Bearer {local_token}"

                    balance = local_db[self.session_name]['Balance']

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
                    await save_log(
                        db_pool=self.db_pool,
                        phone=self.user_data.phone_number,
                        status="ERROR",
                        amount=balance,
                    )

                available_energy = player_data.get('availableTaps', 0)
                new_balance = int(player_data['balanceCoins'])
                calc_taps = new_balance - balance
                balance = new_balance
                total = int(player_data['totalCoins'])
                earn_on_hour = player_data['earnPassivePerHour']

                boosts = player_data['boosts']
                energy_boost_time = boosts.get('BoostFullAvailableTaps', {}).get('lastUpgradeAt', 0)

                logger.success(f"{self.session_name} | Successful tapped! | "
                               f"Balance: <c>{balance}</c> (<g>+{calc_taps}</g>) | Total: <e>{total}</e>")

                local_db[self.session_name]['Balance'] = balance

                await save_log(
                    db_pool=self.db_pool,
                    phone=self.user_data.phone_number,
                    status="TAP",
                    amount=balance,
                )

                if active_turbo is False:
                    if (settings.APPLY_DAILY_ENERGY is True
                            and available_energy < settings.MIN_AVAILABLE_ENERGY
                            and time() - energy_boost_time > 3600):
                        logger.info(f"{self.session_name} | Sleep 5s before apply energy boost")
                        await asyncio.sleep(delay=5)

                        status = await self.apply_boost(http_client=http_client, boost_id="BoostFullAvailableTaps")
                        if status is True:
                            logger.success(f"{self.session_name} | Successfully apply energy boost")

                            await save_log(
                                db_pool=self.db_pool,
                                phone=self.user_data.phone_number,
                                status="APPLY ENERGY BOOST",
                                amount=balance,
                            )

                            await asyncio.sleep(delay=1)

                    if settings.AUTO_UPGRADE is True:
                        upgrades = await self.get_upgrades(http_client=http_client)
                        available_upgrades = [data for data in upgrades if data['isAvailable'] is True]

                        for upgrade in available_upgrades:
                            upgrade_id = upgrade['id']
                            level = upgrade['level']
                            price = upgrade['price']
                            profit = upgrade['profitPerHourDelta']
                            if balance > price and level <= settings.MAX_LEVEL:
                                logger.info(f"{self.session_name} | Sleep 5s before upgrade <e>{upgrade_id}</e>")
                                await asyncio.sleep(delay=10)

                                status = await self.buy_upgrade(http_client=http_client, upgrade_id=upgrade_id)
                                if status is True:
                                    earn_on_hour += profit
                                    logger.success(
                                        f"{self.session_name} | "
                                        f"Successfully upgraded <e>{upgrade_id}</e> to <m>{level}</m> lvl | "
                                        f"Earn every hour: <y>{earn_on_hour}</y> (<g>+{profit}</g>)")

                                    await save_log(
                                        db_pool=self.db_pool,
                                        phone=self.user_data.phone_number,
                                        status="UPGRADE ENERGY",
                                        amount=balance,
                                    )

                                    await asyncio.sleep(delay=1)

                    if available_energy < settings.MIN_AVAILABLE_ENERGY:
                        logger.info(f"{self.session_name} | Minimum energy reached: {available_energy}")
                        logger.info(f"{self.session_name} | Sleep {settings.SLEEP_BY_MIN_ENERGY}s")

                        await asyncio.sleep(delay=settings.SLEEP_BY_MIN_ENERGY)

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, db_pool: async_sessionmaker):
    try:
        async with tg_client:
            user_data = await tg_client.get_me()

        if not local_db.get(tg_client.name):
            local_db[tg_client.name] = {'Token': '', 'Balance': 0}

        proxy = None
        if settings.USE_PROXY_FROM_DB:
            proxy = await get_user_proxy(db_pool=db_pool, phone_number=user_data.phone_number)

        await Tapper(tg_client=tg_client, db_pool=db_pool, user_data=user_data).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
