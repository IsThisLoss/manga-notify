from functools import lru_cache

import pydantic


class Settings(pydantic.BaseSettings):
    tg_token: str                       # telegram bot token
    db_string: str = '/data/db.sqlite'  # path to sqlite database
    db_init: str = './sql/init.sql'     # path to init sql script
    parsing_interval: int  # interval in minutes to run background parsing

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Settings()
