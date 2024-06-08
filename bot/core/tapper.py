import asyncio
import heapq
from random import randint
from time import time

import aiohttp
from aiohttp_proxy import ProxyConnector
from pyrogram import Client

from bot.api.telegram import get_me_telegram
from bot.config import settings
from bot.core.headers import get_headers
from bot.utils.logger import logger
from bot.exceptions import InvalidSession

from bot.api.auth import login
from bot.api.clicker import (
    apply_boost,
    get_profile_data,
    get_upgrades,
    buy_upgrade,
    get_boosts,
    claim_daily_cipher,
    send_taps,
    get_config,
)
from bot.api.exchange import select_exchange
from bot.api.tasks import get_tasks, get_daily
from bot.utils.scripts import decode_cipher
from bot.utils.tg_web_data import get_tg_web_data
from bot.utils.proxy import check_proxy


class Tapper:
    def __init__(self, tg_client: Client):
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def run(self, proxy: str | None) -> None:
        access_token_created_time = 0
        turbo_time = 0
        active_turbo = False

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None
        http_client = aiohttp.ClientSession(
            headers=get_headers(), connector=proxy_conn
        )

        if proxy:
            await check_proxy(
                http_client=http_client,
                proxy=proxy,
                session_name=self.session_name,
            )

        tg_web_data = await get_tg_web_data(
            tg_client=self.tg_client,
            proxy=proxy,
            session_name=self.session_name,
        )

        while True:
            try:
                if http_client.closed:
                    if proxy_conn and not proxy_conn.closed:
                        proxy_conn.close()

                    proxy_conn = (
                        ProxyConnector().from_url(proxy) if proxy else None
                    )
                    http_client = aiohttp.ClientSession(
                        headers=get_headers(), connector=proxy_conn
                    )

                if time() - access_token_created_time >= 3600:
                    access_token = await self.refresh_access_token(
                        http_client, tg_web_data
                    )
                    if not access_token:
                        continue

                    access_token_created_time = time()

                profile_data, game_config = await self.get_game_data(
                    http_client
                )
                await self.log_profile_info(profile_data)

                available_energy = profile_data.get('availableTaps', 0)
                balance = int(profile_data.get('balanceCoins', 0))

                upgrades = await get_upgrades(http_client=http_client)
                tasks = await get_tasks(http_client=http_client)

                await self.handle_daily_tasks(http_client, tasks)
                await self.handle_daily_cipher(http_client, game_config)
                await self.select_exchange_if_needed(http_client, profile_data)

                taps, active_turbo, turbo_time = await self.calculate_taps(
                    active_turbo, turbo_time
                )

                player_data = await self.send_taps_and_update_balance(
                    http_client, available_energy, balance, taps
                )

                if not player_data:
                    continue

                (
                    available_energy,
                    balance,
                    earn_on_hour,
                ) = self.update_player_data(player_data, balance)

                if not active_turbo and settings.AUTO_UPGRADE:
                    (
                        balance,
                        earn_on_hour,
                        upgrades,
                    ) = await self.handle_upgrades(
                        http_client, balance, earn_on_hour, upgrades
                    )

                if available_energy < settings.MIN_AVAILABLE_ENERGY:
                    await self.handle_low_energy(
                        http_client,
                        proxy_conn,
                        available_energy,
                        access_token_created_time,
                    )

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f'{self.session_name} | Unknown error: {error}')
                await asyncio.sleep(delay=3)

            else:
                await self.sleep_between_taps(active_turbo)

    @staticmethod
    async def refresh_access_token(http_client, tg_web_data):
        access_token = await login(
            http_client=http_client, tg_web_data=tg_web_data
        )
        if not access_token:
            return None

        http_client.headers['Authorization'] = f'Bearer {access_token}'
        await get_me_telegram(http_client=http_client)
        return access_token

    @staticmethod
    async def get_game_data(http_client):
        game_config = await get_config(http_client=http_client)
        profile_data = await get_profile_data(http_client=http_client)
        return profile_data, game_config

    async def log_profile_info(self, profile_data):
        last_passive_earn = profile_data['lastPassiveEarn']
        earn_on_hour = profile_data['earnPassivePerHour']
        logger.info(
            f'{self.session_name} | Last passive earn: <g>+{last_passive_earn:,}</g> | '
            f'Earn every hour: <y>{earn_on_hour:,}</y>'
        )

    async def handle_daily_tasks(self, http_client, tasks):
        daily_task = tasks[-1]
        rewards = daily_task['rewardsByDays']
        is_completed = daily_task['isCompleted']
        days = daily_task['days']

        await asyncio.sleep(delay=2)

        if not is_completed:
            status = await get_daily(http_client=http_client)
            if status:
                logger.success(
                    f'{self.session_name} | Successfully get daily reward | '
                    f"Days: <m>{days}</m> | Reward coins: {rewards[days - 1]['rewardCoins']}"
                )

    async def handle_daily_cipher(self, http_client, game_config):
        await asyncio.sleep(delay=2)

        daily_cipher = game_config.get('dailyCipher')
        if daily_cipher:
            cipher = daily_cipher['cipher']
            bonus = daily_cipher['bonusCoins']
            is_claimed = daily_cipher['isClaimed']

            if not is_claimed and cipher:
                decoded_cipher = decode_cipher(cipher=cipher)
                status = await claim_daily_cipher(
                    http_client=http_client, cipher=decoded_cipher
                )
                if status:
                    logger.success(
                        f'{self.session_name} | Successfully claim daily cipher: <y>{decoded_cipher}</y> | '
                        f'Bonus: <g>+{bonus:,}</g>'
                    )

    async def select_exchange_if_needed(self, http_client, profile_data):
        await asyncio.sleep(delay=2)

        exchange_id = profile_data.get('exchangeId')
        if not exchange_id:
            status = await select_exchange(
                http_client=http_client, exchange_id='bybit'
            )
            if status:
                logger.success(
                    f'{self.session_name} | Successfully selected exchange <y>Bybit</y>'
                )

    @staticmethod
    async def calculate_taps(active_turbo, turbo_time):
        taps = randint(
            a=settings.RANDOM_TAPS_COUNT[0], b=settings.RANDOM_TAPS_COUNT[1]
        )

        if active_turbo:
            taps += settings.ADD_TAPS_ON_TURBO
            if time() - turbo_time > 20:
                active_turbo = False
                turbo_time = 0

        return taps, active_turbo, turbo_time

    async def send_taps_and_update_balance(
        self, http_client, available_energy, balance, taps
    ):
        player_data = await send_taps(
            http_client=http_client,
            available_energy=available_energy,
            taps=taps,
        )

        if not player_data:
            return None

        new_balance = int(player_data.get('balanceCoins', 0))
        calc_taps = new_balance - balance
        total = int(player_data.get('totalCoins', 0))

        logger.success(
            f'{self.session_name} | Successful tapped! | Balance: <c>{new_balance:,}</c> (<g>+{calc_taps:,}</g>) | '
            f'Total: <e>{total:,}</e>'
        )

        return player_data

    @staticmethod
    def update_player_data(player_data, balance):
        available_energy = player_data.get('availableTaps', 0)
        new_balance = int(player_data.get('balanceCoins', 0))
        earn_on_hour = player_data['earnPassivePerHour']
        return available_energy, new_balance, earn_on_hour

    async def handle_upgrades(
        self, http_client, balance, earn_on_hour, upgrades
    ):
        for _ in range(settings.UPGRADES_COUNT):
            available_upgrades = self.get_available_upgrades(upgrades)
            if not available_upgrades:
                continue

            top_card = self.get_top_upgrade(
                available_upgrades, balance, earn_on_hour
            )

            if not top_card:
                continue

            upgrade = top_card[2]
            upgrade_id = upgrade['id']
            level = upgrade['level']
            price = upgrade['price']
            profit = upgrade['profitPerHourDelta']

            logger.info(
                f'{self.session_name} | Sleep 5s before upgrade <e>{upgrade_id}</e>'
            )
            await asyncio.sleep(delay=5)

            status, new_upgrades = await buy_upgrade(
                http_client=http_client, upgrade_id=upgrade_id
            )

            if status:
                earn_on_hour += profit
                balance -= price
                logger.success(
                    f'{self.session_name} | Successfully upgraded <e>{upgrade_id}</e> with price <r>{price:,}</r> to <m>{level}</m> lvl | '
                    f'Earn every hour: <y>{earn_on_hour:,}</y> (<g>+{profit:,}</g>) | Money left: <e>{balance:,}</e>'
                )

                await asyncio.sleep(delay=1)
                if new_upgrades:
                    upgrades = new_upgrades
                break
            else:
                await asyncio.sleep(delay=1)

        return balance, earn_on_hour, upgrades

    @staticmethod
    def get_available_upgrades(upgrades):
        return [
            data
            for data in upgrades
            if data['isAvailable']
            and not data['isExpired']
            and data.get('cooldownSeconds', 0) == 0
            and data.get('maxLevel', data['level']) >= data['level']
            and (
                data.get('condition') is None
                or data['condition'].get('_type') != 'SubscribeTelegramChannel'
            )
        ]

    @staticmethod
    def get_top_upgrade(available_upgrades, balance, earn_on_hour):
        queue = []

        for upgrade in available_upgrades:
            upgrade_id = upgrade['id']
            level = upgrade['level']
            price = upgrade['price']
            profit = upgrade['profitPerHourDelta']

            significance = profit / max(price, 1)

            free_money = balance - settings.BALANCE_TO_SAVE
            max_price_limit = earn_on_hour * 5

            if (
                (free_money * 0.7) >= price
                and level <= settings.MAX_LEVEL
                and profit > 0
                and price < max_price_limit
            ):
                heapq.heappush(queue, (-significance, upgrade_id, upgrade))

        if not queue:
            return None

        return heapq.nsmallest(1, queue)[0]

    async def handle_low_energy(
        self,
        http_client,
        proxy_conn,
        available_energy,
        access_token_created_time,
    ):
        boosts = await get_boosts(http_client=http_client)
        energy_boost = next(
            (
                boost
                for boost in boosts
                if boost['id'] == 'BoostFullAvailableTaps'
            ),
            {},
        )

        if (
            settings.APPLY_DAILY_ENERGY
            and energy_boost.get('cooldownSeconds', 0) == 0
            and energy_boost.get('level', 0) <= energy_boost.get('maxLevel', 0)
        ):
            logger.info(
                f'{self.session_name} | Sleep 5s before apply energy boost'
            )
            await asyncio.sleep(delay=5)

            status = await apply_boost(
                http_client=http_client, boost_id='BoostFullAvailableTaps'
            )
            if status:
                logger.success(
                    f'{self.session_name} | Successfully apply energy boost'
                )

                await asyncio.sleep(delay=1)
                return

        await http_client.close()
        if proxy_conn and not proxy_conn.closed:
            proxy_conn.close()

        random_sleep = randint(
            settings.SLEEP_BY_MIN_ENERGY[0], settings.SLEEP_BY_MIN_ENERGY[1]
        )

        logger.info(
            f'{self.session_name} | Minimum energy reached: {available_energy}'
        )
        logger.info(f'{self.session_name} | Sleep {random_sleep:,}s')

        await asyncio.sleep(delay=random_sleep)
        access_token_created_time = 0

    @staticmethod
    async def sleep_between_taps(active_turbo):
        sleep_between_clicks = randint(
            a=settings.SLEEP_BETWEEN_TAP[0], b=settings.SLEEP_BETWEEN_TAP[1]
        )

        if active_turbo:
            sleep_between_clicks = 4

        logger.info(f'Sleep {sleep_between_clicks}s')
        await asyncio.sleep(delay=sleep_between_clicks)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f'{tg_client.name} | Invalid Session')
