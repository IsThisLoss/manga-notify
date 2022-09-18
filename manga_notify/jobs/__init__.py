import arq

from . import background_parsing
from . import send_telegram_message
from . import remind_later

from .. import dependencies


async def run():
    deps = dependencies.get()
    cfg = deps.get_cfg()
    redis = await deps.get_queues()

    async def on_startup(ctx):
        ctx['deps'] = deps

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
                microsecond=cfg.parsing_interval * 60000,
            )
        ],
        redis_pool=redis,
        on_startup=on_startup,
    )
    await worker.async_run()
