import heapq
import asyncio
from time import time
from random import randint
from datetime import datetime, timedelta

import aiohttp
from aiohttp_proxy import ProxyConnector
from pyrogram import Client

from bot.api.combo import claim_daily_combo, get_combo_cards
from bot.api.telegram import get_me_telegram
from bot.config import settings
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
from bot.api.tasks import get_nuxt_builds, get_tasks, get_airdrop_tasks, get_daily
from bot.utils.scripts import decode_cipher, get_headers
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

        headers = get_headers(name=self.tg_client.name)

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        http_client = aiohttp.ClientSession(
            headers=headers,
            connector=proxy_conn
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
                    if proxy_conn:
                        if not proxy_conn.closed:
                            proxy_conn.close()

                    proxy_conn = (
                        ProxyConnector().from_url(proxy) if proxy else None
                    )
                    http_client = aiohttp.ClientSession(
                        headers=headers, connector=proxy_conn
                    )

                if time() - access_token_created_time >= 3600:
                    http_client.headers.pop('Authorization', None)

                    await get_nuxt_builds(http_client=http_client)

                    access_token = await login(
                        http_client=http_client,
                        tg_web_data=tg_web_data,
                        session_name=self.session_name,
                    )

                    if not access_token:
                        continue

                    http_client.headers['Authorization'] = f'Bearer {access_token}'

                    access_token_created_time = time()

                    await get_me_telegram(http_client=http_client)
                    game_config = await get_config(http_client=http_client)

                    profile_data = await get_profile_data(http_client=http_client)

                    last_passive_earn = profile_data['lastPassiveEarn']
                    earn_on_hour = profile_data['earnPassivePerHour']

                    logger.info(f'{self.session_name} | Last passive earn: <lg>+{last_passive_earn:,}</lg> | '
                                f'Earn every hour: <ly>{earn_on_hour:,}</ly>')

                    available_energy = profile_data.get('availableTaps', 0)
                    balance = int(profile_data.get('balanceCoins', 0))

                    upgrades_data = await get_upgrades(http_client=http_client)

                    upgrades = upgrades_data['upgradesForBuy']
                    daily_combo = upgrades_data.get('dailyCombo')
                    if daily_combo:
                        bonus = daily_combo['bonusCoins']
                        is_claimed = daily_combo['isClaimed']
                        upgraded_list = daily_combo['upgradeIds']

                        if not is_claimed:
                            combo_cards = await get_combo_cards(
                                http_client=http_client
                            )

                            cards = combo_cards['combo']
                            date = combo_cards['date']

                            available_combo_cards = [
                                data for data in upgrades
                                if data['isAvailable'] is True
                                and data['id'] in cards
                                and data['id'] not in upgraded_list
                                and data['isExpired'] is False
                                and data.get('cooldownSeconds', 0) == 0
                                and data.get('maxLevel', data['level']) >= data['level']
                            ]

                            start_bonus_round = datetime.strptime(date, "%d-%m-%y").replace(hour=15)
                            end_bonus_round = start_bonus_round + timedelta(days=1)

                            if start_bonus_round <= datetime.now() < end_bonus_round:
                                common_price = sum([upgrade['price'] for upgrade in available_combo_cards])
                                need_cards_count = len(cards)
                                possible_cards_count = len(available_combo_cards)
                                is_combo_accessible = need_cards_count == possible_cards_count

                                if not is_combo_accessible:
                                    logger.info(f"{self.session_name} | "
                                                f"<lr>Daily combo is not applicable</lr>, you can only purchase {possible_cards_count} of {need_cards_count} cards")

                                if balance < common_price:
                                    logger.info(f"{self.session_name} | "
                                                f"<lr>Daily combo is not applicable</lr>, you don't have enough coins. Need <ly>{common_price:,}</ly> coins, but your balance is <lr>{balance:,}</lr> coins")

                                if common_price < settings.MAX_COMBO_PRICE and balance > common_price and is_combo_accessible:
                                    for upgrade in available_combo_cards:
                                        upgrade_id = upgrade['id']
                                        level = upgrade['level']
                                        price = upgrade['price']
                                        profit = upgrade['profitPerHourDelta']

                                        logger.info(
                                            f'{self.session_name} | '
                                            f'Sleep 5s before upgrade <lr>combo</lr> card <le>{upgrade_id}</le>'
                                        )

                                        await asyncio.sleep(delay=5)

                                        status, upgrades = await buy_upgrade(
                                            http_client=http_client,
                                            upgrade_id=upgrade_id,
                                        )

                                        if status is True:
                                            earn_on_hour += profit
                                            balance -= price
                                            logger.success(
                                                f'{self.session_name} | '
                                                f'Successfully upgraded <le>{upgrade_id}</le> with price <lr>{price:,}</lr> to <m>{level}</m> lvl | '
                                                f'Earn every hour: <ly>{earn_on_hour:,}</ly> (<lg>+{profit:,}</lg>) | '
                                                f'Money left: <le>{balance:,}</le>'
                                            )

                                            await asyncio.sleep(delay=1)

                                    await asyncio.sleep(delay=2)

                                    status = await claim_daily_combo(
                                        http_client=http_client
                                    )
                                    if status is True:
                                        logger.success(
                                            f'{self.session_name} | Successfully claimed daily combo | '
                                            f'Bonus: <lg>+{bonus:,}</lg>'
                                        )

                    tasks = await get_tasks(http_client=http_client)

                    daily_task = tasks[-1]
                    rewards = daily_task['rewardsByDays']
                    is_completed = daily_task['isCompleted']
                    days = daily_task['days']

                    await asyncio.sleep(delay=2)

                    if is_completed is False:
                        status = await get_daily(http_client=http_client)
                        if status is True:
                            logger.success(
                                f'{self.session_name} | Successfully get daily reward | '
                                f"Days: <lm>{days}</lm> | Reward coins: <lg>+{rewards[days - 1]['rewardCoins']}</lg>"
                            )

                    await asyncio.sleep(delay=2)

                    airdrop_tasks = await get_airdrop_tasks(http_client=http_client)

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
                            if status is True:
                                logger.success(
                                    f'{self.session_name} | '
                                    f'Successfully claim daily cipher: <ly>{decoded_cipher}</ly> | '
                                    f'Bonus: <lg>+{bonus:,}</lg>'
                                )

                        await asyncio.sleep(delay=2)

                    exchange_id = profile_data.get('exchangeId')
                    if not exchange_id:
                        status = await select_exchange(
                            http_client=http_client, exchange_id='bybit'
                        )
                        if status is True:
                            logger.success(
                                f'{self.session_name} | Successfully selected exchange <ly>Bybit</ly>'
                            )

                taps = randint(
                    a=settings.RANDOM_TAPS_COUNT[0],
                    b=settings.RANDOM_TAPS_COUNT[1],
                )

                if active_turbo:
                    taps += settings.ADD_TAPS_ON_TURBO
                    if time() - turbo_time > 20:
                        active_turbo = False
                        turbo_time = 0

                player_data = await send_taps(
                    http_client=http_client,
                    available_energy=available_energy,
                    taps=taps,
                )

                if not player_data:
                    continue

                available_energy = player_data.get('availableTaps', 0)
                new_balance = int(player_data.get('balanceCoins', 0))
                calc_taps = new_balance - balance
                balance = new_balance
                total = int(player_data.get('totalCoins', 0))
                earn_on_hour = player_data['earnPassivePerHour']

                logger.success(
                    f'{self.session_name} | Successful tapped! | '
                    f'Balance: <c>{balance:,}</c> (<lg>+{calc_taps:,}</lg>) | Total: <le>{total:,}</le>'
                )

                if active_turbo is False:
                    if settings.AUTO_UPGRADE is True:
                        for _ in range(settings.UPGRADES_COUNT):
                            available_upgrades = [
                                data
                                for data in upgrades
                                if data['isAvailable'] is True
                                and data['isExpired'] is False
                                and data.get('cooldownSeconds', 0) == 0
                                and data.get('maxLevel', data['level']) >= data['level']
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

                                if (
                                        (free_money * 0.7) >= price
                                        and level <= settings.MAX_LEVEL
                                        and profit > 0
                                        and price < max_price_limit
                                ):
                                    heapq.heappush(
                                        queue,
                                        (-significance, upgrade_id, upgrade),
                                    )

                            if not queue:
                                continue

                            top_card = heapq.nsmallest(1, queue)[0]

                            upgrade = top_card[2]

                            upgrade_id = upgrade['id']
                            level = upgrade['level']
                            price = upgrade['price']
                            profit = upgrade['profitPerHourDelta']

                            logger.info(
                                f'{self.session_name} | Sleep 5s before upgrade <le>{upgrade_id}</le>'
                            )
                            await asyncio.sleep(delay=5)

                            status, upgrades = await buy_upgrade(
                                http_client=http_client, upgrade_id=upgrade_id
                            )

                            if status is True:
                                earn_on_hour += profit
                                balance -= price
                                logger.success(
                                    f'{self.session_name} | '
                                    f'Successfully upgraded <le>{upgrade_id}</le> with price <lr>{price:,}</lr> to <m>{level}</m> lvl | '
                                    f'Earn every hour: <ly>{earn_on_hour:,}</ly> (<lg>+{profit:,}</lg>) | '
                                    f'Money left: <le>{balance:,}</le>'
                                )

                                await asyncio.sleep(delay=1)

                                continue

                    if available_energy < settings.MIN_AVAILABLE_ENERGY:
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
                                settings.APPLY_DAILY_ENERGY is True
                                and energy_boost.get('cooldownSeconds', 0) == 0
                                and energy_boost.get('level', 0)
                                <= energy_boost.get('maxLevel', 0)
                        ):
                            logger.info(
                                f'{self.session_name} | Sleep 5s before apply energy boost'
                            )
                            await asyncio.sleep(delay=5)

                            status = await apply_boost(
                                http_client=http_client,
                                boost_id='BoostFullAvailableTaps',
                            )
                            if status is True:
                                logger.success(
                                    f'{self.session_name} | Successfully apply energy boost'
                                )

                                await asyncio.sleep(delay=1)

                                continue

                        await http_client.close()
                        if proxy_conn:
                            if not proxy_conn.closed:
                                proxy_conn.close()

                        random_sleep = randint(
                            settings.SLEEP_BY_MIN_ENERGY[0],
                            settings.SLEEP_BY_MIN_ENERGY[1],
                        )

                        logger.info(
                            f'{self.session_name} | Minimum energy reached: <ly>{available_energy:.0f}</ly>'
                        )
                        logger.info(
                            f'{self.session_name} | Sleep {random_sleep:,}s'
                        )

                        await asyncio.sleep(delay=random_sleep)

                        access_token_created_time = 0

            except InvalidSession as error:
                raise error

            except Exception as error:
                logger.error(f'{self.session_name} | Unknown error: {error}')
                await asyncio.sleep(delay=3)

            else:
                sleep_between_clicks = randint(
                    a=settings.SLEEP_BETWEEN_TAP[0],
                    b=settings.SLEEP_BETWEEN_TAP[1],
                )

                if active_turbo is True:
                    sleep_between_clicks = 4

                logger.info(f'Sleep {sleep_between_clicks}s')
                await asyncio.sleep(delay=sleep_between_clicks)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f'{tg_client.name} | Invalid Session')
