from ..feed_processing import parsing_job
from ..channels import telegram_channel
from .. import dependencies


async def job(ctx: dict):
    """
    Запускается по расписанию
    """

    deps: dependencies.Dependencies = ctx['deps']
    redis = await deps.get_queues()
    channel_factory = telegram_channel.TelegramChannelFactory(redis)
    db = await deps.get_db()
    await parsing_job.run_background_parsing(db, channel_factory)
