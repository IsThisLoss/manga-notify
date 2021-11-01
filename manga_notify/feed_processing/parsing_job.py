import logging

from . import feed_processor
from . import subscription

from ..channels import channel
from ..database import database


def run_background_parsing(db: database.DataBase, channel_factory: channel.ChannelFactory):
    """
    Запускает парсинг всех фидов
    """
    logging.info('Run background parsing')
    feeds = db.feeds.get_all()
    logging.info(f'Got {len(feeds)} feeds')
    processor = feed_processor.get_feed_processor()
    feed_subscription = subscription.FeedSubscription(db.users.get_all())

    for feed in feeds:
        subscribed_users = feed_subscription.get_subscribed_users(feed)
        channels = channel_factory.get_channels(subscribed_users)
        if not channels:
            logging.info(f'Got no channels for feed {feed.get_id()}')
            continue
        with db.transaction():
            feed = processor.process(feed, channels)
            db.feeds.update(feed.get_id(), feed.get_cursor())
