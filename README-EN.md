[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/sho6ot)
[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue">](https://www.python.org/downloads/)


![demo](.github/images/demo.png)


> 🇷🇺 README на русском доступен [здесь](README.md)


## ⚙ [Settings](.env-example)
<details>
  <summary><b>API_ID / API_HASH</b> - Platform Data</summary>
  <p>These values are necessary for authorization and working with the Telegram API. Without them, the bot will not be able to connect to your account.</p>
  <ul>
    <li><strong>Example:</strong></li>
    <code>API_ID=2182472</code>
    <br>
    <code>API_HASH=b592f0d605a1b67c20e8d1c7582f20</code>
  </ul>
</details>

<details>
  <summary><b>MIN_AVAILABLE_ENERGY</b> - Minimum Energy Level</summary>
  <p>This setting determines the minimum energy level at which the bot will go idle to simulate human-like activity.</p>
  <ul>
    <li><strong>Example:</strong> <code>200</code></li>
    <li><strong>Default:</strong> <code>200</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_BY_MIN_ENERGY</b> - Delay at Minimum Energy</summary>
  <p>Sets a pause in the bot's operation if the energy drops below the set minimum. This simulates human-like activity.</p>
  <ul>
    <li><strong>Example:</strong> <code>[1800,3600]</code></li>
    <li><strong>Default:</strong> <code>[1800,3600]</code></li>
  </ul>
</details>

<details>
  <summary><b>AUTO_UPGRADE</b> - Auto Upgrade Passive Earnings</summary>
  <p>This parameter determines whether the bot will automatically upgrade your cards to increase passive income.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>False</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_LEVEL</b> - Maximum Upgrade Level</summary>
  <p>Determines the maximum level up to which the bot will upgrade your cards.</p>
  <ul>
    <li><strong>Example:</strong> <code>20</code></li>
    <li><strong>Default:</strong> <code>20</code></li>
  </ul>
</details>

<details>
  <summary><b>MIN_PROFIT</b> - Minimum Upgrade Profit</summary>
  <p>Determines the minimum profit of the card that the bot will upgrade.</p>
  <ul>
    <li><strong>Example:</strong> <code>1000</code></li>
    <li><strong>Default:</strong> <code>1000</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_PRICE</b> - Maximum Upgrade Price</summary>
  <p>Sets the limit on the amount the bot can spend on a single card upgrade.</p>
  <ul>
    <li><strong>Example:</strong> <code>50000000</code></li>
    <li><strong>Default:</strong> <code>50000000</code></li>
  </ul>
</details>

<details>
  <summary><b>BALANCE_TO_SAVE</b> - Balance Limit</summary>
  <p>This parameter defines the minimum balance that the bot will guarantee to keep, without spending it on upgrades or purchases.</p>
  <ul>
    <li><strong>Example:</strong> <code>1000000</code></li>
    <li><strong>Default:</strong> <code>1000000</code></li>
  </ul>
</details>

<details>
  <summary><b>UPGRADES_COUNT</b> - Number of Upgrades per Cycle</summary>
  <p>Specifies how many cards the bot will upgrade in one cycle to always choose the most profitable card.</p>
  <ul>
    <li><strong>Example:</strong> <code>10</code></li>
    <li><strong>Default:</strong> <code>10</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_COMBO_PRICE</b> - Maximum Combo Card Purchase Price</summary>
  <p>Defines the maximum amount the bot can spend on purchasing combo cards when the balance is sufficient.</p>
  <ul>
    <li><strong>Example:</strong> <code>10000000</code></li>
    <li><strong>Default:</strong> <code>10000000</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_COMBO</b> - Use Combo Cards</summary>
  <p>Allows the bot to activate combo cards to gain bonuses.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_PROMO_CODES</b> - Activate Promo Codes</summary>
  <p>Allows the bot to automatically enter and activate promo codes in the Playground section to obtain keys.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_CIPHER</b> - Enter Daily Cipher</summary>
  <p>Enables automatic entry of the daily Morse code cipher to obtain bonuses.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_REWARD</b> - Collect Daily Reward</summary>
  <p>The bot will automatically collect daily rewards if this parameter is enabled.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_ENERGY</b> - Activate Daily Energy Boost</summary>
  <p>Allows the bot to activate the daily energy boost to replenish energy.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_MINI_GAME</b> - Play Mini Game</summary>
  <p>Setting that allows the bot to automatically play daily mini-games to obtain keys.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_MINI_GAME_TILES</b> - Delay in the mini game TILES</summary>
  <p>Option to set a random delay from the start of the game to its end.</p>
  <ul>
    <li><strong>Example:</strong> <code>[600,900]</code></li>
    <li><strong>Default:</strong> <code>[600,900]</code></li>
  </ul>
</details>

<details>
  <summary><b>SCORE_MINI_GAME_TILES</b> - Maximum score for the game TILES</summary>
  <p>Sets the random score that will be reached in the game.</p>
  <ul>
    <li><strong>Example:</strong> <code>[300,500]</code></li>
    <li><strong>Default:</strong> <code>[300,500]</code></li>
  </ul>
</details>

<details>
  <summary><b>GAMES_COUNT</b> - Number of games in TILES</summary>
  <p>Defines the random number of games that the bot will play in one cycle.</p>
  <ul>
    <li><strong>Example:</strong> <code>[1,10]</code></li>
    <li><strong>Default:</strong> <code>[1,10]</code></li>
  </ul>
</details>

<details>
  <summary><b>AUTO_COMPLETE_TASKS</b> - Complete Tasks</summary>
  <p>This feature allows the bot to automatically complete tasks if they are available.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_TAPS</b> - Use Taps</summary>
  <p>Determines whether the bot will use taps (clicks).</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_TAPS_COUNT</b> - Random Taps Count</summary>
  <p>This parameter defines the range of random tap (click) counts the bot may use at once.</p>
  <ul>
    <li><strong>Example:</strong> <code>[10,50]</code></li>
    <li><strong>Default:</strong> <code>[10,50]</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_BETWEEN_TAP</b> - Delay Between Taps</summary>
  <p>Sets the interval time between taps (clicks). This prevents too frequent tapping.</p>
  <ul>
    <li><strong>Example:</strong> <code>[10,25]</code></li>
    <li><strong>Default:</strong> <code>[10,25]</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_RANDOM_DELAY_IN_RUN</b> - Use Random Delay at Startup</summary>
  <p>This setting allows for random delays for each account before starting the bot, helping to start each account separately rather than simultaneously.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>False</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_DELAY_IN_RUN</b> - Random Delay at Startup</summary>
  <p>Defines the range of random delay applied to each account before starting the bot. This helps to start each account separately rather than simultaneously.</p>
  <ul>
    <li><strong>Example:</strong> <code>[0,15]</code></li>
    <li><strong>Default:</strong> <code>[0,15]</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_RANDOM_USERAGENT</b> - Use Random User Agent</summary>
  <p>When enabled, the bot will use random User-Agents for each account and save them in `profiles.json` for future use, to increase anonymity and protection against bans.</p>
  <ul>
    <li><strong>Example:</strong> <code>True / False</code></li>
    <li><strong>Default:</strong> <code>False</code></li>
  </ul>
</details>


## 📕 [Profiles](profiles.json)
For each session, you can create a profile with unique data:
```json
{
  "session1": {
    "tonAddress": "UQCvE0cNCpBoD6JQ0tFSIGXVissDQGNk6OoBQ8UTlkaQ5lLB",
    "proxy": "http://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {},
    "fingerprint": {}
  },
  "session2": {
    "tonAddress": "UQCvE0cNCpBoD6JQ0tFSIGXVissDQGNk6OoBQ8UTlkaQ5lLB",
    "proxy": "socks5://yGow3a:uBro3wL@58.195.21.83:9715",
    "headers": {},
    "fingerprint": {}
  }
}
```
> ❕ Note: session1 and session2 are example session names.  
> If headers or fingerprint are empty, [default](bot/utils/default.py) data will be used.  
> Field `tonAddress` connects TON wallet to game, if there is no connected address.


## ⚡ Quick Start
1. To install the libraries on Windows, run `INSTALL.bat` or `install.sh` on Linux.
2. To start the bot, use `START.bat` (or in the console: python main.py) if you use Windows or `start.sh` on Linux.


## 📌 Prerequisites
Before you start, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) version 3.10 or 3.11.


## 📃 Getting API keys
1. Go to [my.telegram.org](https://my.telegram.org) and log in using your phone number.
2. Select **"API development tools"** and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` in the `.env` file, provided after registering your application.


## 🧱 Installation
You can download the [**Repository**](https://github.com/shamhi/HamsterKombatBot) by cloning it to your system and installing the required dependencies:
```shell
~ >>> git clone https://github.com/shamhi/HamsterKombatBot.git 
~ >>> cd HamsterKombatBot

# Linux
~/HamsterKombatBot >>> python3 -m venv venv
~/HamsterKombatBot >>> source venv/bin/activate
~/HamsterKombatBot >>> pip3 install -r requirements.txt
~/HamsterKombatBot >>> cp .env-example .env
~/HamsterKombatBot >>> nano .env  # Enter your API_ID and API_HASH
~/HamsterKombatBot >>> python3 main.py

# Windows
~/HamsterKombatBot >>> python -m venv venv
~/HamsterKombatBot >>> venv\Scripts\activate
~/HamsterKombatBot >>> pip install -r requirements.txt
~/HamsterKombatBot >>> copy .env-example .env
~/HamsterKombatBot >>> # Open the .env file and enter your API_ID and API_HASH
~/HamsterKombatBot >>> python main.py
```
> To install as a Linux service for background operation of the bot, see [here](docs/LINUX-SERVIS-INSTALL.md).


⏳ For a quick start, you can also use arguments, for example:
```shell
~/HamsterKombatBot >>> python3 main.py --action (1/2)
# Или
~/HamsterKombatBot >>> python3 main.py -a (1/2)

# 1 - Creates a session
# 2 - Starts the bot
```
