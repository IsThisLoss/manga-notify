import typing
import logging

from ..database import database
from ..database import feed_storage

from . import feed_processor


class FeedManager:
    """
    Controls feeds creation
    on feeds creation launch its
    parsing to obtain last cursor
    on parsing error, feed won't be created
    """

    def __init__(self, db: database.DataBase):
        self._db = db
        self._processor = feed_processor.get_feed_processor()

    async def find_or_create(
        self,
        driver: str,
        url: str,
    ) -> typing.Optional[feed_storage.FeedData]:
        feed = await self._db.feeds.find(driver, url)
        if not feed:
            feed = await self._create_feed(driver, url)
        return feed

    async def _create_feed(
        self,
        driver: str,
        url: str,
    ) -> typing.Optional[feed_storage.FeedData]:
        feed = None
        try:
            async with self._db.transaction():
                feed = await self._create_feed_impl(driver, url)
        except Exception:
            logging.exception(
                'Failed to parse feed on its creation, '
                f'driver = {driver}, url = {url}'
            )
        return feed

    async def _create_feed_impl(
        self,
        driver: str,
        url: str,
    ) -> typing.Optional[feed_storage.FeedData]:
        feed = await self._db.feeds.create(driver, url)
        if not feed:
            return None
        feed = await self._processor.process(feed)
        if not feed:
            return None
        await self._db.feeds.update(
            feed.get_id(),
            feed.get_cursor(),
            feed.get_title(),
        )
        return feed
