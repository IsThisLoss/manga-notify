import typing
import logging

from ..drivers import driver_factory
from ..database import feed_storage
from ..channels import channel


class FeedProcessor:
    """
    Process updates of one feed
    """

    def __init__(self, drivers: driver_factory.DriverFactory):
        self._drivers = drivers

    def process(
        self,
        feed: feed_storage.FeedData,
        channels: typing.List[channel.Channel]
    ) -> feed_storage.FeedData:
        logging.info(f'Going to parse feed_id = {feed.get_id()}')
        driver = self._drivers.get(feed.get_driver())
        parsed = driver.parse(feed)
        logging.info(f'Parsed {len(parsed.messages)} messages')
        self._send_to_channels(channels, parsed.messages)
        logging.info('Flush')
        return parsed.feed_data

    def _send_to_channels(
            self,
            channels: typing.List[channel.Channel],
            messages: typing.List[channel.Message]
    ):
        for channel in channels: 
            if not messages:
                continue
            # send only last message of feed
            try:
                channel.send(messages[-1])
            except Exception:
                logging.exception("Failed to send message to channel")
