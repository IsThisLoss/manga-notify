import contextlib
import logging
import typing

import asyncpg

from . import feed_storage
from . import user_storage


class DataBase:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool
        self._reinit(self._pool)

    def _reinit(self, conn: typing.Union[asyncpg.Pool, asyncpg.Connection]):
        self._users = user_storage.UserStorage(conn)
        self._feeds = feed_storage.FeedStorage(conn)

    @property
    def users(self) -> user_storage.UserStorage:
        return self._users

    @property
    def feeds(self) -> feed_storage.FeedStorage:
        return self._feeds

    @contextlib.asynccontextmanager
    async def transaction(self):
        async with self._pool.acquire() as connection:
            async with connection.transaction() as _:
                logging.info('Start transaction')
                self._reinit(connection)
                try:
                    yield
                finally:
                    logging.info('End transaction')
                    self._reinit(self._pool)
