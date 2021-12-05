import typing
import logging

from ..database import database
from ..database import feed_storage
from ..database import user_storage

from . import feed_manager


class FeedSubscription:
    """
    Gain users subscribed to specific channel
    """
    def __init__(self, users: typing.List[user_storage.UserInfo]):
        self._users = users

    def get_subscribed_users(
        self,
        feed: feed_storage.FeedData,
    ) -> typing.List[str]:
        result = []
        for user in self._users:
            if feed.get_id() in user.subscriptions:
                result.append(user.user_id)
        return result


class UserSubscription:
    """
    Provides api to get all user's feed
    subscribe and unsubscribe user for specific feed
    with some validations
    """

    def __init__(self, db: database.DataBase):
        self._db = db

    def get_user_feeds(
        self,
        user_id: str,
    ) -> typing.List[feed_storage.FeedData]:
        result: typing.List[feed_storage.FeedData] = []
        user_info = self._db.users.get_subscriptions(user_id)
        if not user_info:
            return result
        for feed_id in user_info.subscriptions:
            feed = self._db.feeds.get(feed_id)
            if not feed:
                continue
            result.append(feed)
        return result

    def subscribe(self, user_id: str, driver: str, url: str) -> bool:
        feed_mgr = feed_manager.FeedManager(self._db)
        feed = feed_mgr.find_or_create(driver, url)
        if not feed:
            return False
        try:
            self._db.users.subscribe(user_id, feed.get_id())
            return True
        except Exception:
            logging.exception(
                f'Cannot subscribe user {user_id} to feed {feed.get_id()}'
            )
        return False

    def unsubscribe(self, user_id: str, driver: str, url: str) -> bool:
        feed = self._db.feeds.find(driver, url)
        if not feed:
            return False
        try:
            self._db.users.unsubscribe(user_id, feed.get_id())
            return True
        except Exception:
            logging.exception(
                f'Cannot unsubscribe user {user_id} from feed {feed.get_id()}'
            )
        return False
