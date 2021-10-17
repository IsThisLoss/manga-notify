import telegram
import telegram.ext

from .feed_processing import parsing_job
from .database import get_database
from .channels import channel_factory


def job(context: telegram.ext.CallbackContext):
    db = get_database()
    channels = channel_factory.ChannelFactory(context.bot)
    parsing_job.run_background_parsing(db, channels)
