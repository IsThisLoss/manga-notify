import typing

import asyncpg


class FeedData:
    def __init__(self, id, driver, url, cursor):
        self._id = id
        self._driver = driver
        self._url = url
        self._cursor = cursor

    def get_id(self) -> int:
        return self._id

    def get_driver(self) -> str:
        return self._driver

    def get_cursor(self) -> str:
        return self._cursor

    def get_url(self) -> str:
        return self._url

    def set_cursor(self, cursor):
        self._cursor = cursor


class FeedStorage:
    def __init__(self, conn: asyncpg.Connection):
        self._connection = conn

    async def get_all(self) -> typing.List[FeedData]:
        rows = await self._connection.fetch("""
            SELECT
                id, driver, url, cursor
            FROM
                feeds
        """)
        result = []
        for id, driver, url, cursor in rows:
            data = FeedData(
                id=id,
                driver=driver,
                url=url,
                cursor=cursor,
            )
            result.append(data)
        return result

    async def get(self, id: int) -> typing.Optional[FeedData]:
        row = await self._connection.fetchrow("""
            SELECT
                id, driver, url, cursor
            FROM
                feeds
            WHERE
                id = $1
            LIMIT 1
        """, id)
        if not row:
            return None
        return FeedData(
            id=row[0],
            driver=row[1],
            url=row[2],
            cursor=row[3],
        )

    async def find(self, driver: str, url: str) -> typing.Optional[FeedData]:
        row = await self._connection.fetchrow("""
            SELECT
                id,
                driver,
                url,
                cursor
            FROM
                feeds
            WHERE
                driver = $1 AND url = $2
            LIMIT 1
        """, driver, url)
        if not row:
            return None
        id, driver, url, cursor = row
        return FeedData(
            id=id,
            driver=driver,
            url=url,
            cursor=cursor,
        )

    async def create(self, driver: str, url: str) -> typing.Optional[FeedData]:
        id = await self._connection.fetchval("""
            INSERT INTO
                feeds(driver, url)
            VALUES
                ($1, $2)
            RETURNING id
        """, driver, url)
        if not id:
            return None
        return FeedData(
            id=id,
            driver=driver,
            url=url,
            cursor='',
        )

    async def update(self, id: int, cursor: str):
        await self._connection.execute("""
            UPDATE
                feeds
            SET
                cursor = $1
            WHERE
                id = $2
        """, cursor, id)
