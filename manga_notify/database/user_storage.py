import collections
import dataclasses
import logging
import typing

import asyncpg


@dataclasses.dataclass(frozen=True)
class UserInfo:
    user_id: str
    subscriptions: typing.Set[int]


class UserStorage:
    def __init__(self, conn: asyncpg.Connection):
        self._connection = conn

    async def _exec(self, query, *args) -> bool:
        try:
            await self._connection.execute(query, *args)
            return True
        except Exception:
            logging.exception("Failed to exequte query")
        return False

    async def exists(self, user_id: str) -> bool:
        """
        return true if gived user_id was found in database
        """
        val = await self._connection.fetchval("""
            SELECT EXISTS(SELECT id FROM users WHERE id = $1)
        """, user_id)
        return bool(val)

    async def register(self, user_id: str, login: str):
        return await self._exec("""
            INSERT INTO users (
                id,
                login
            )
            VALUES ($1, $2)
            ON CONFLICT (id) DO NOTHING
        """, user_id, login)

    async def subscribe(self, user_id: str, feed_id: int):
        await self._exec("""
            INSERT INTO
                subscriptions (user_id, feed_id)
            VALUES ($1, $2)
            ON CONFLICT (user_id, feed_id) DO NOTHING
        """, user_id, feed_id)

    async def unsubscribe(self, user_id: str, feed_id: int):
        await self._exec("""
            DELETE FROM
                subscriptions
            WHERE
                user_id = $1
                AND
                feed_id = $2
        """, user_id, feed_id)

    async def get_subscriptions(self, user_id: str) -> UserInfo:
        rows = await self._connection.fetch("""
            SELECT
                subscriptions.feed_id as feed_id
            FROM
                users
                INNER JOIN
                subscriptions
                ON users.id = subscriptions.user_id
            WHERE
                users.id = $1
        """, user_id)
        feed_ids = set()
        for feed_id in rows:
            feed_ids.add(int(feed_id[0]))
        return UserInfo(
            user_id=user_id,
            subscriptions=feed_ids,
        )

    async def get_all(self) -> typing.List[UserInfo]:
        rows = await self._connection.fetch("""
            SELECT
                users.id as user_id,
                subscriptions.feed_id as feed_id
            FROM
                users
                INNER JOIN
                subscriptions
                ON users.id = subscriptions.user_id
        """)
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
