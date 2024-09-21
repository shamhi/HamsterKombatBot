from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any, Union, Dict, List, Optional, Tuple


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: float = 0
    API_HASH: str = ''

    SLEEP_TIME: Union[List[int], int] = [2700, 8100]

    AUTO_UPGRADE: bool = False
    MAX_LEVEL: int = 20
    MIN_PROFIT: float = 0.000001
    MAX_PRICE: float = 500.0

    BALANCE_TO_SAVE: float = 0.000001
    UPGRADES_COUNT: int = 10

    APPLY_PROMO_CODES: bool = True
    APPLY_DAILY_MINI_GAME: bool = True

    SLEEP_MINI_GAME_TILES: List[int] = [600, 900]
    SCORE_MINI_GAME_TILES: List[int] = [300, 500]
    GAMES_COUNT: List[int] = [1, 10]

    AUTO_COMPLETE_TASKS: bool = True

    USE_RANDOM_DELAY_IN_RUN: bool = False
    RANDOM_DELAY_IN_RUN: List[int] = [0, 15]

    USE_RANDOM_USERAGENT: bool = False


settings = Settings()
