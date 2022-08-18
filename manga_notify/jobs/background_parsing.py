from ..feed_processing import parsing_job
from ..database import get_database
from ..channels import telegram_channel

async def job(ctx: dict):
    """
    Запускается по расписанию
    """

    redis = ctx['redis']
    channel_factory = telegram_channel.TelegramChannelFactory(redis)
    async with get_database() as db:
        await parsing_job.run_background_parsing(db, channel_factory)
