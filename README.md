[<img src="https://img.shields.io/badge/Telegram-%40Me-orange">](https://t.me/sho6ot)
[<img src="https://img.shields.io/badge/python-3.10%20%7C%203.11-blue">](https://www.python.org/downloads/)

> 🇪🇳 README in english available [here](README-EN.md)

![demo image](.github/images/demo.png)


## ⚙ [Настройки](.env-example)
<details>
  <summary><b>API_ID / API_HASH</b> - Данные платформы</summary>
  <p>Эти значения необходимы для авторизации и работы с Telegram API. Без них бот не сможет подключиться к вашему аккаунту.</p>
  <ul>
    <li><strong>Пример:</strong></li>
    <code>API_ID=2182472</code>
    <br>
    <code>API_HASH=b592f0d605a1b67c20e8d1c7582f20</code>
  </ul>
</details>

<details>
  <summary><b>MIN_AVAILABLE_ENERGY</b> - Минимальное количество энергии</summary>
  <p>Эта настройка определяет минимальный уровень энергии, при котором бот будет уходить в сон, чтобы повторить человеческую активность.</p>
  <ul>
    <li><strong>Пример:</strong> <code>535</code></li>
    <li><strong>Дефолт:</strong> <code>200</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_BY_MIN_ENERGY</b> - Задержка при минимальной энергии</summary>
  <p>Устанавливает паузу в работе бота, если энергия опускается ниже установленного минимума. Это повторить человеческую активность.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[2000,3300]</code></li>
    <li><strong>Дефолт:</strong> <code>[1800,3600]</code></li>
  </ul>
</details>

<details>
  <summary><b>AUTO_UPGRADE</b> - Улучшение пассивного заработка</summary>
  <p>Этот параметр определяет, будет ли бот автоматически прокачивать ваши карты для повышения пассивного дохода.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>False</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_LEVEL</b> - Максимальный уровень апгрейда</summary>
  <p>Определяет максимальный уровень, до которого бот будет прокачивать ваши карты.</p>
  <ul>
    <li><strong>Пример:</strong> <code>15</code></li>
    <li><strong>Дефолт:</strong> <code>20</code></li>
  </ul>
</details>

<details>
  <summary><b>MIN_PROFIT</b> - Минимальная прибыль карты</summary>
  <p>Определяет минимальную прибыль карты, которую прокачает бот.</p>
  <ul>
    <li><strong>Пример:</strong> <code>2500</code></li>
    <li><strong>Дефолт:</strong> <code>1000</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_PRICE</b> - Максимальная цена апгрейда</summary>
  <p>Устанавливает лимит на сумму, которую бот может потратить на одно улучшение карты.</p>
  <ul>
    <li><strong>Пример:</strong> <code>20000000</code></li>
    <li><strong>Дефолт:</strong> <code>50000000</code></li>
  </ul>
</details>

<details>
  <summary><b>BALANCE_TO_SAVE</b> - Лимит баланса</summary>
  <p>Этот параметр определяет минимальный остаток на балансе, который бот гарантировано сохранит, не тратя его на улучшения или покупки.</p>
  <ul>
    <li><strong>Пример:</strong> <code>2000</code></li>
    <li><strong>Дефолт:</strong> <code>1000000</code></li>
  </ul>
</details>

<details>
  <summary><b>UPGRADES_COUNT</b> - Количество апгрейдов за один круг</summary>
  <p>Задает, сколько карт бот будет прокачивать за один цикл работы, чтобы каждый раз выбирать самую выгодную карту из всех.</p>
  <ul>
    <li><strong>Пример:</strong> <code>5</code></li>
    <li><strong>Дефолт:</strong> <code>10</code></li>
  </ul>
</details>

<details>
  <summary><b>MAX_COMBO_PRICE</b> - Максимальная цена покупки комбо карт</summary>
  <p>Определяет максимальную сумму, которую бот может потратить на покупку комбо-карт при достаточном балансе.</p>
  <ul>
    <li><strong>Пример:</strong> <code>15000000</code></li>
    <li><strong>Дефолт:</strong> <code>10000000</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_COMBO</b> - Использование комбо карт</summary>
  <p>Настройка позволяет боту активировать комбо-карты для получения бонусов.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_PROMO_CODES</b> - Активация промокодов</summary>
  <p>Позволяет боту автоматически вводить и активировать промокоды на игры в разделе Playground для получения ключей.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_CIPHER</b> - Ввод ежедневного шифра</summary>
  <p>Включает возможность автоматического ввода ежедневного шифра азбуки морзе для получения бонусов.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_REWARD</b> - Сбор ежедневной награды</summary>
  <p>Бот будет автоматически собирать ежедневные награды, если этот параметр активен.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_ENERGY</b> - Активация ежедневного буста энергии</summary>
  <p>Позволяет боту активировать ежедневный буст энергии для ее восполнения.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>APPLY_DAILY_MINI_GAME</b> - Прохождение мини игры</summary>
  <p>Настройка, позволяющая автоматически проходить ежедневные мини-игры для получения ключей.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_MINI_GAME_TILES</b> - Задержка в мини игре TILES</summary>
  <p>Опция для установления рандомной задержки от начала игры до ее конца.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[500,800]</code></li>
    <li><strong>Дефолт:</strong> <code>[600,900]</code></li>
  </ul>
</details>

<details>
  <summary><b>SCORE_MINI_GAME_TILES</b> - Максимальный счет для игры TILES</summary>
  <p>Устанавливает рандомный счет, который будет достигнут в игре.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[250,600]</code></li>
    <li><strong>Дефолт:</strong> <code>[300,500]</code></li>
  </ul>
</details>

<details>
  <summary><b>GAMES_COUNT</b> - Количество игр в TILES</summary>
  <p>Определяет рандомное количество игр, которые сыграет бот в одном цикле.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[3,15]</code></li>
    <li><strong>Дефолт:</strong> <code>[1,10]</code></li>
  </ul>
</details>

<details>
  <summary><b>AUTO_COMPLETE_TASKS</b> - Выполнение заданий</summary>
  <p>Эта функция позволяет боту автоматически выполнять задачи, если они доступны.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_TAPS</b> - Использование тапов</summary>
  <p>Определяет, будет ли бот использовать тапы (клики).</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
        <li><strong>Дефолт:</strong> <code>True</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_TAPS_COUNT</b> - Рандомное количество тапов</summary>
  <p>Этот параметр определяет диапазон случайного количества тапов (кликов), которые бот может тапнуть за один раз.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[25,100]</code></li>
    <li><strong>Дефолт:</strong> <code>[10,50]</code></li>
  </ul>
</details>

<details>
  <summary><b>SLEEP_BETWEEN_TAP</b> - Задержка между тапами</summary>
  <p>Устанавливает интервал времени между тапами (кликами). Это предотвращает слишком частое нажатие.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[5,15]</code></li>
    <li><strong>Дефолт:</strong> <code>[10,25]</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_RANDOM_DELAY_IN_RUN</b> - Использование рандомной задержки при запуске</summary>
  <p>Эта настройка позволяет использовать случайные задержки для каждого аккаунта перед началом бота, что помогает запустить каждый аккаунт по отдельности, а не одновременно.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>False</code></li>
  </ul>
</details>

<details>
  <summary><b>RANDOM_DELAY_IN_RUN</b> - Рандомная задержка при запуске</summary>
  <p>Определяет диапазон случайной задержки, которая применяется для каждого аккаунта перед началом бота. Это помогает запустить каждый аккаунт по отдельности, а не одновременно.</p>
  <ul>
    <li><strong>Пример:</strong> <code>[0,20]</code></li>
    <li><strong>Дефолт:</strong> <code>[0,15]</code></li>
  </ul>
</details>

<details>
  <summary><b>USE_RANDOM_USERAGENT</b> - Использование рандомного User Agent</summary>
  <p>При активации этого параметра бот будет использовать случайные User-Agent для каждого аккаунта и сохранит их в `sessions/profiles.json` для дальнейшего использования, чтобы повысить уровень анонимности и защиты от блокировок.</p>
  <ul>
    <li><strong>Пример:</strong> <code>True / False</code></li>
    <li><strong>Дефолт:</strong> <code>False</code></li>
  </ul>
</details>


## 📕 [Профили](profiles.json)
Для каждой сессии можно создать профиль с уникальными данными:
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
> [!NOTE]
> `session1` и `session2` - это примеры названий сессий.  
> Если `headers` или `fingerprint` пусты, то возьмутся [дефолтные](bot/utils/default.py) значения.  
> Поле `tonAddress` подключает TON кошелек к игре, если нет подключенного.


## ⚡ Быстрый старт
1. Чтобы установить библиотеки в Windows, запустите `INSTALL.bat` или `install.sh` на Linux.
2. Для запуска бота используйте `START.bat` (или в консоли: `python main.py`) если вы используете Windows или `start.sh` на Linux.


## 📌 Зависимости
Прежде чем начать, убедитесь, что у вас установлено следующее:
- [Python](https://www.python.org/downloads/) версии 3.10 или 3.11.


## 📃 Получение API ключей
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org) и войдите в систему, используя свой номер телефона.
2. Выберите **"API development tools"** и заполните форму для регистрации нового приложения.
3. Запишите `API_ID` и `API_HASH` в файле `.env`, предоставленные после регистрации вашего приложения.


## 🧱 Установка
Вы можете клонировать [**Репозиторий**](https://github.com/shamhi/HamsterKombatBot) на вашу систему и установить необходимые зависимости:
```shell
~ >>> git clone https://github.com/shamhi/HamsterKombatBot.git 
~ >>> cd HamsterKombatBot

# Linux
~/HamsterKombatBot >>> python3 -m venv venv
~/HamsterKombatBot >>> source venv/bin/activate
~/HamsterKombatBot >>> pip3 install -r requirements.txt
~/HamsterKombatBot >>> cp .env-example .env
~/HamsterKombatBot >>> nano .env  # Укажите ваши API_ID и API_HASH
~/HamsterKombatBot >>> python3 main.py

# Windows
~/HamsterKombatBot >>> python -m venv venv
~/HamsterKombatBot >>> venv\Scripts\activate
~/HamsterKombatBot >>> pip install -r requirements.txt
~/HamsterKombatBot >>> copy .env-example .env
~/HamsterKombatBot >>> # Откройте файл .env и укажите ваши API_ID и API_HASH
~/HamsterKombatBot >>> python main.py
```

> [!TIP]
> Установка в качестве Linux службы для фоновой работы бота [тут](docs/LINUX-SERVIS-INSTALL.md).


⏳ Также для быстрого запуска вы можете использовать аргументы, например:
```shell
~/HamsterKombatBot >>> python3 main.py --action [1/2]
# Или
~/HamsterKombatBot >>> python3 main.py -a [1/2]

# 1 - Создает сессию
# 2 - Запускает бота
```
