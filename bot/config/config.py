from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    MIN_AVAILABLE_ENERGY: int = 200
    SLEEP_BY_MIN_ENERGY: int = 200

    ADD_TAPS_ON_TURBO: int = 2500

    AUTO_UPGRADE: bool = True
    MAX_LEVEL: int = 7

    APPLY_DAILY_ENERGY: bool = True
    APPLY_DAILY_TURBO: bool = False

    RANDOM_TAPS_COUNT: list[int] = [50, 200]
    SLEEP_BETWEEN_TAP: list[int] = [50, 70]

    USE_PROXY_FROM_FILE: bool = False

    IGNORED_UPGRADES: list[str] = ['save_hamsters_from_drowning']


settings = Settings()
