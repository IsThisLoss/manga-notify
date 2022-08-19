# flake8: noqa: E402
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


import os
import asyncio
import argparse

from . import bot
from . import settings
from . import jobs

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


async def main():
    parser = argparse.ArgumentParser('Manga notify')
    parser.add_argument('mode', metavar='MODE', help='Run mode: bot or jobs')
    args = parser.parse_args()

    cfg = settings.get_config()
    init(cfg)
    if args.mode == 'bot':
        await bot.dp.start_polling()
    elif args.mode == 'jobs':
        await jobs.run()
    else:
        logging.fatal(f'Unknow mode: {args.mode}')
        exit(1)


if __name__ == '__main__':
    asyncio.run(main())
