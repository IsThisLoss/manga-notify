import typing
import logging

from ..drivers import driver_factory
from ..database import feed_storage
from ..channels import channel


class FeedProcessor:
    """
    Execute feeds processing
    1) Choose driver
    2) Launch parsing
    3) Send new messages
    """

    def __init__(self, drivers: driver_factory.DriverFactory):
        self._drivers = drivers

    def process(
        self,
        feed: feed_storage.FeedData,
        channels: typing.Optional[typing.List[channel.Channel]] = None
    ) -> feed_storage.FeedData:
        logging.info(f'Going to parse feed_id = {feed.get_id()}')
        driver = self._drivers.get(feed.get_driver())
        parsed = driver.parse(feed)
        logging.info(f'Parsed {len(parsed.messages)} messages')
        if channels:
            self._send_to_channels(channels, parsed.messages)
        logging.info('Flush')
        return parsed.feed_data

    def _send_to_channels(
            self,
            channels: typing.List[channel.Channel],
            messages: typing.List[channel.Message]
    ):
        if not messages:
            return
        for current_channel in channels:
            for message in messages:
                try:
                    current_channel.send(message)
                except Exception:
                    logging.exception("Failed to send message to channel")


def get_feed_processor():
    return FeedProcessor(driver_factory.DriverFactory())
