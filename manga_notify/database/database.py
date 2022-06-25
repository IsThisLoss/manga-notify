import contextlib
import logging

from . import feed_storage
from . import user_storage


class DataBase:
    def __init__(self, connection):
        self._connection = connection
        self._users = user_storage.UserStorage(self._connection)
        self._feeds = feed_storage.FeedStorage(self._connection)

    @property
    def users(self) -> user_storage.UserStorage:
        return self._users

    @property
    def feeds(self) -> feed_storage.FeedStorage:
        return self._feeds

    @contextlib.asynccontextmanager
    async def transaction(self):
        try:
            await self._connection.execute('BEGIN')
            yield
            await self._connection.execute('COMMIT')
        except Exception:
            self._connection.execute('ROLLBACK')
            logging.warning('Rollback transaction')
            raise
