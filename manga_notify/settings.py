import typing
from functools import lru_cache

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    tg_token: str                       # telegram bot token

    redis_host: str = 'localhost'       # redis host
    redis_port: int = 6379              # redis port
    redis_password: typing.Optional[str] = None         # redis password

    # postgres connection string
    pg_conn: str = (
        'postgresql://manga_notify:manga_notify@localhost:5432/manga_notify'
    )

    # prefix for redis
    # keys used by aiogram fsm
    aiogram_fsm_prefix: 'str' = 'aiogram_fsm'

    parsing_interval: int  # interval in minutes to run background parsing

    # Token to access erai-raws
    erai_raws_token: typing.Optional[str] = None

    # Outgoing http requests timeout in seconds
    http_client_timeout: float = 30

    # Port for incoming request from reverse proxy
    web_server_port: int = 8080
    # Path to webhook route, on which Telegram will send requests
    webhook_path: str = "/webhook"
    # Secret key to validate requests from Telegram
    webhook_secret: str = "secret"
    # Base URL for webhook will be used to generate webhook URL for Telegram,
    base_webhook_url: str = "https://localhost/"

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Settings()
