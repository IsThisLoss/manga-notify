from functools import lru_cache

import pydantic


class Settings(pydantic.BaseSettings):
    tg_token: str                       # telegram bot token

    redis_host: str = 'localhost'       # redis host
    redis_port: int = 6379              # redis port

    # postgres connection string
    pg_conn: str = (
        'postgresql://manga_notify:manga_notify@localhost:5432/manga_notify'
    )

    # prefix for redis
    # keys used by aiogram fsm
    aiogram_fsm_prefix: 'str' = 'aiogram_fsm'

    parsing_interval: int  # interval in minutes to run background parsing

    class Config:
        env_file = '.env'



@lru_cache()
def get_config():
    return Settings()
