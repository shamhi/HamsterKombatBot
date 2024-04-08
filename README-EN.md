[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/sho6ot)


![img1](.github/images/demo.png)

> 🇷🇺 README на русском доступен [здесь](README.md)

## Functionality
| Functional                                                     | Supported |
|----------------------------------------------------------------|:---------:|
| Multithreading                                                 |     ✅     |
| Binding a proxy to a session                                   |     ✅     |
| Auto-purchase of items if you have coins (tap, energy, charge) |     ✅     |
| Random sleep time between clicks                               |     ✅     |
| Random number of clicks per request                            |     ✅     |
| Support tdata / pyrogram .session / telethon .session          |     ✅     |

## [Settings](https://github.com/shamhi/HamsterKombatBot/blob/main/.env-example)
| Настройка                | Описание                                                                                 |
|--------------------------|------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**    | Platform data from which to launch a Telegram session _(stock - Android)_                |
| **MIN_AVAILABLE_ENERGY** | Minimum amount of available energy, upon reaching which there will be a delay _(eg 100)_ |
| **SLEEP_BY_MIN_ENERGY**  | Delay when reaching minimum energy in seconds _(eg 200)_                                 |
| **AUTO_UPGRADE**         | Whether to upgrade the passive earn _(True / False)_                                     |
| **MAX_LEVEL**            | Maximum upgrade level _(eg 20)_                                                          |
| **APPLY_DAILY_ENERGY**   | Whether to use the daily free energy boost _(True / False)_                              |
| **APPLY_DAILY_TURBO**    | Whether to use the daily free turbo boost _(True / False)_                               |
| **RANDOM_CLICKS_COUNT**  | Random number of taps _(eg 50,200)_                                                      |
| **SLEEP_BETWEEN_TAP**    | Random delay between taps in seconds _(eg 10,25)_                                        |
| **USE_PROXY_FROM_FILE**  | Whether to use proxy from the `bot/config/proxies.txt` file (True / False)               |

## Installation
You can download [**Repository**](https://github.com/shamhi/HamsterKombatBot) by cloning it to your system and installing the necessary dependencies:
```shell
~ >>> git clone https://github.com/shamhi/HamsterKombatBot.git
~ >>> cd HamsterKombatBot

# If you are using Telethon sessions, then clone the "converter" branch
~ >>> git clone https://github.com/shamhi/HamsterKombatBot.git -b converter
~ >>> cd HamsterKombatBot

#Linux
~/HamsterKombatBot >>> python3 -m venv venv
~/HamsterKombatBot >>> source venv/bin/activate
~/HamsterKombatBot >>> pip3 install -r requirements.txt
~/HamsterKombatBot >>> cp .env-example .env
~/HamsterKombatBot >>> nano .env # Here you must specify your API_ID and API_HASH , the rest is taken by default
~/HamsterKombatBot >>> python3 main.py

#Windows
~/HamsterKombatBot >>> python -m venv venv
~/HamsterKombatBot >>> venv\Scripts\activate
~/HamsterKombatBot >>> pip install -r requirements.txt
~/HamsterKombatBot >>> copy .env-example .env
~/HamsterKombatBot >>> # Specify your API_ID and API_HASH, the rest is taken by default
~/HamsterKombatBot >>> python main.py
```

Also for quick launch you can use arguments, for example:
```shell
~/HamsterKombatBot >>> python3 main.py --action (1/2)
# Or
~/HamsterKombatBot >>> python3 main.py -a (1/2)

#1 - Create session
#2 - Run clicker
```
