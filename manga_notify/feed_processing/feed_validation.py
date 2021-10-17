import logging

from . import feed_processor

from ..channels import dummy_channel
from ..drivers import driver_factory
from ..database import feed_storage


def get_last_cursor(feed: feed_storage.FeedData) -> feed_storage.FeedData:
    processor = feed_processor.FeedProcessor(driver_factory.DriverFactory())
    channel = dummy_channel.DummyChannel()
    feed = processor.process(feed, [channel])
    if channel.count <=0:
        raise ValueError("Empty feed")
    logging.info(f'Got last cursour = {feed.get_cursor()} for feed_id = {feed.get_id()}')
    return feed
