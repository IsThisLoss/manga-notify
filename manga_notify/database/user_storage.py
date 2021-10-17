import collections
import dataclasses
import logging
import typing

import sqlite3


@dataclasses.dataclass(frozen=True)
class UserInfo:
    user_id: str
    subscriptions: typing.Set[int]


class UserStorage:
    def __init__(self, conn: sqlite3.Connection):
        self._connection = conn

    def _exec(self, query, args=None) -> bool:
        try:
            self._connection.execute(query, args or [])
            return True
        except Exception:
            logging.exception("Failed to exequte query")
        return False

    def register(self, user_id: str):
        return self._exec("""
            INSERT INTO
                users (id)
            VALUES (?)
            ON CONFLICT (id) DO NOTHING
        """, (user_id,))

    def subscribe(self, user_id: str, feed_id: int):
        self._exec("""
            INSERT INTO
                subscriptions (user_id, feed_id)
            VALUES (?, ?)
            ON CONFLICT (user_id, feed_id) DO NOTHING
        """, (user_id, feed_id))

    def unsubscribe(self, user_id: str, feed_id: int):
        self._exec("""
            DELETE FROM
                subscriptions
            WHERE
                user_id = ?
                AND
                feed_id = ?
        """, (user_id, feed_id))

    def get_subscriptions(self, user_id: str) -> UserInfo:
        rows = self._connection.execute("""
            SELECT
                subscriptions.feed_id as feed_id
            FROM
                users
                INNER JOIN
                subscriptions
                ON users.id = subscriptions.user_id
            WHERE
                users.id = ?
        """, (user_id,)).fetchall()
        feed_ids = set()
        for feed_id in rows:
            feed_ids.add(int(feed_id[0]))
        return UserInfo(
            user_id=user_id,
            subscriptions=feed_ids,
        )

    def get_all(self) -> typing.List[UserInfo]:
        rows = self._connection.execute("""
            SELECT
                users.id as user_id,
                subscriptions.feed_id as feed_id
            FROM
                users
                INNER JOIN
                subscriptions
                ON users.id = subscriptions.user_id
        """).fetchall()
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
