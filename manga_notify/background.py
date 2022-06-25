from .feed_processing import parsing_job
from .database import get_database
from .channels import telegram_channel
from .bot import bot


async def job():
    """
    Запускается по расписанию
    """
    channels_factory = telegram_channel.TelegramChannelFactory(bot)
    async with get_database() as db:
        await parsing_job.run_background_parsing(db, channels_factory)
