import logging
from datetime import datetime
import typing

import arq

from . import background_parsing
from . import send_telegram_message
from . import remind_later

from .. import dependencies


def gen_minutes(interval: int) -> typing.Set[int]:
    start = datetime.now().minute
    result = set()
    for minute in range(start, 60, interval):
        result.add(minute)
    for minute in range(start, 0, -interval):
        result.add(minute)
    return result


async def run():
    deps = dependencies.get()
    cfg = deps.get_cfg()
    redis = await deps.get_queues()

    async def on_startup(ctx):
        ctx['deps'] = deps

    logging.info('Parsing interval is %s mins', cfg.parsing_interval)
    minutes = gen_minutes(cfg.parsing_interval)
    logging.info(
        'Going to run cron at %s minutes of hour',
        ','.join(map(str, sorted(minutes))),
    )

    worker = arq.worker.Worker(
        functions=[
            arq.worker.func(
                send_telegram_message.job, name='send_telegram_message'
            ),
            arq.worker.func(
                remind_later.job, name='remind_later'
            ),
        ],
        cron_jobs=[
            arq.cron(
                background_parsing.job,
                name='background_parsing',
                minute=minutes,
            )
        ],
        redis_pool=redis,
        on_startup=on_startup,
    )
    await worker.async_run()
