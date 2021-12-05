import telegram
import telegram.ext

from .feed_processing import parsing_job
from .database import get_database
from .channels import telegram_channel


def job(context: telegram.ext.CallbackContext):
    """
    Запускается по расписанию бибилиотекой python telegram bot
    """
    db = get_database()
    channels_factory = telegram_channel.TelegramChannelFactory(context.bot)
    parsing_job.run_background_parsing(db, channels_factory)
    """ very long string very long stringvery long stringvery long stringvery long stringvery long stringvery long stringvery long string"""
