import contextlib
import logging

import sqlite3

from . import feed_storage
from . import user_storage


class DataBase:
    def __init__(self, conn_string):
        self._connection = sqlite3.connect(
            conn_string,
            isolation_level=None,
        )
        self._users = user_storage.UserStorage(self._connection)
        self._feeds = feed_storage.FeedStorage(self._connection)

    @property
    def users(self) -> user_storage.UserStorage:
        return self._users

    @property
    def feeds(self) -> feed_storage.FeedStorage:
        return self._feeds

    def __del__(self):
        self._connection.close()

    @contextlib.contextmanager
    def transaction(self):
        try:
            self._connection.execute('BEGIN')
            yield
            self._connection.execute('COMMIT')
        except Exception:
            self._connection.execute('ROLLBACK')
            logging.warning('Rollback transaction')
            raise
