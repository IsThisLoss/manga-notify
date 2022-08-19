import arq

from . import background_parsing
from . import send_telegram_message

from .. import settings


async def run():
    cfg = settings.get_config()

    redis_settings = arq.connections.RedisSettings(
        host=cfg.redis_host,
        port=cfg.redis_port,
    )

    worker = arq.worker.Worker(
        functions=[
            arq.worker.func(
                send_telegram_message.job, name='send_telegram_message'
            ),
        ],
        cron_jobs=[
            arq.cron(
                background_parsing.job,
                name='background_parsing',
                microsecond=cfg.parsing_interval * 60000,
            )
        ],
        redis_settings=redis_settings,
    )
    await worker.async_run()
