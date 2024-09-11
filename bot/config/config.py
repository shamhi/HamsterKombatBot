from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Union, Dict, List, Optional, Tuple


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int = 0
    API_HASH: str = ''

    MIN_AVAILABLE_ENERGY: int = 200
    SLEEP_BY_MIN_ENERGY: List[int] = [1800, 3600]

    AUTO_UPGRADE: bool = False
    MAX_LEVEL: int = 20
    MIN_PROFIT: int = 1000
    MAX_PRICE: int = 50000000

    BALANCE_TO_SAVE: int = 1000000
    UPGRADES_COUNT: int = 10

    MAX_COMBO_PRICE: int = 10000000

    APPLY_COMBO: bool = True
    APPLY_PROMO_CODES: bool = True
    APPLY_DAILY_CIPHER: bool = True
    APPLY_DAILY_REWARD: bool = True
    APPLY_DAILY_ENERGY: bool = True
    APPLY_DAILY_MINI_GAME: bool = True

    SLEEP_MINI_GAME_TILES: List[int] = [600, 900]
    SCORE_MINI_GAME_TILES: List[int] = [300, 500]
    GAMES_COUNT: List[int] = [1, 10]

    AUTO_COMPLETE_TASKS: bool = True

    USE_TAPS: bool = True
    RANDOM_TAPS_COUNT: List[int] = [10, 50]
    SLEEP_BETWEEN_TAP: List[int] = [10, 25]

    USE_RANDOM_DELAY_IN_RUN: bool = False
    RANDOM_DELAY_IN_RUN: List[int] = [0, 15]

    USE_RANDOM_USERAGENT: bool = False


settings = Settings()
