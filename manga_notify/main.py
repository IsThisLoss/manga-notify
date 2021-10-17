import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


import datetime

from . import bot
from . import background
from . import settings

import telegram.ext


def main():
    cfg = settings.get_config()
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
