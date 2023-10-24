import collections
import dataclasses
import logging
import os
import typing

import aiosql
import asyncpg


CUR_DIR = os.path.dirname(os.path.abspath(__file__))

queries = aiosql.from_path(
    CUR_DIR + '/sql/user_storage.sql',
    'asyncpg',
)


@dataclasses.dataclass(frozen=True)
class UserInfo:
    user_id: str
    subscriptions: typing.Set[int]


class UserStorage:
    def __init__(
        self,
        conn: typing.Union[asyncpg.Pool, asyncpg.Connection],
    ):
        self._connection = conn

    async def exists(self, user_id: str) -> bool:
        """
        return true if gived user_id was found in database
        """
        val = await queries.exists(
            self._connection,
            id=user_id,
        )
        return bool(val)

    async def register(self, user_id: str, login: str):
        try:
            await queries.insert(
                self._connection,
                id=user_id,
                login=login,
            )
            return True
        except Exception:
            logging.exception('Failed to register user %s', user_id)
        return False

    async def subscribe(self, user_id: str, feed_id: int):
        await queries.subscribe(
            self._connection,
            user_id=user_id,
            feed_id=feed_id,
        )

    async def unsubscribe(self, user_id: str, feed_id: int):
        await queries.unsubscribe(
            self._connection,
            user_id=user_id,
            feed_id=feed_id,
        )

    async def get_subscriptions(self, user_id: str) -> UserInfo:
        rows = await queries.get_subscriptions(
            self._connection,
            user_id=user_id,
        )
        feed_ids = set()
        for feed_id in rows:
            feed_ids.add(int(feed_id[0]))
        return UserInfo(
            user_id=user_id,
            subscriptions=feed_ids,
        )

    async def get_all(self) -> typing.List[UserInfo]:
        rows = await queries.get_all_subscriptions(
            self._connection,
        )
        user_to_subscription = collections.defaultdict(set)
        for user_id, feed_id in rows:
            user_to_subscription[user_id].add(int(feed_id))

        result = []
        for user_id, feed_ids in user_to_subscription.items():
            result.append(UserInfo(
                user_id=user_id,
                subscriptions=feed_ids,
            ))
        return result
