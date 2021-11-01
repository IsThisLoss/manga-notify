import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


import os
import datetime

from . import bot
from . import background
from . import settings

import sqlite3
import telegram.ext


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
    

def main():
    cfg = settings.get_config()
    init(cfg)
    updater = telegram.ext.Updater(token=cfg.tg_token)
    dispatcher = bot.make_dispatcher(updater)
    dispatcher.job_queue.run_repeating(
        background.job,
        datetime.timedelta(minutes=cfg.parsing_interval)
    )
    dispatcher.job_queue.start()
    updater.start_polling()


if __name__ == '__main__':
    main()
