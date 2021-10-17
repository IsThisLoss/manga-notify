import logging

from . import feed_processor

from ..channels import channel_factory
from ..database import database
from ..drivers import driver_factory


def run_background_parsing(db: database.DataBase, channel_factory: channel_factory.ChannelFactory):
    logging.info('Run background parsing')
    feeds = db.feeds.get_all()
    processor = feed_processor.FeedProcessor(driver_factory.DriverFactory())
    users = db.users.get_all()
    for feed in feeds:
        channels = channel_factory.get_channels(feed, users)
        if not channels:
            continue
        with db.transaction():
            feed = processor.process(feed, channels)
            db.feeds.update(feed.get_id(), feed.get_cursor())
