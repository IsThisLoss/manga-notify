# flake8: noqa: E402
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


import os
import asyncio

from . import bot
from . import background
from . import settings

import sqlite3


def init(cfg: settings.Settings):
    """
    Needs to initialize database
    on first run
    """
    if os.path.exists(cfg.db_string):
        return
    if not os.path.exists(cfg.db_init):
        logging.error(f'Cannot find {cfg.db_init} file')
        return
    with open(cfg.db_init) as f:
        conn = sqlite3.connect(cfg.db_string)
        conn.executescript(f.read())


async def bg_work():
    while True:
        await background.job()
        await asyncio.sleep(settings.get_config().parsing_interval * 60)


async def main():
    cfg = settings.get_config()
    init(cfg)
    task = asyncio.create_task(bg_work())
    try:
        await bot.dp.start_polling()
    finally:
        task.cancel()


if __name__ == '__main__':
    asyncio.run(main())
