import typing

import aiosqlite


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
    def __init__(self, conn: aiosqlite.Connection):
        self._connection = conn

    async def get_all(self) -> typing.List[FeedData]:
        rows = await self._connection.execute("""
            SELECT
                id, driver, url, cursor
            FROM
                feeds
        """)
        result = []
        async for id, driver, url, cursor in rows:
            data = FeedData(
                id=id,
                driver=driver,
                url=url,
                cursor=cursor,
            )
            result.append(data)
        return result

    async def get(self, id: int) -> typing.Optional[FeedData]:
        cur = await self._connection.execute("""
            SELECT
                id, driver, url, cursor
            FROM
                feeds
            WHERE
                id = ?
            LIMIT 1
        """, (id,))
        row = await cur.fetchone()
        if not row:
            return None
        return FeedData(
            id=row[0],
            driver=row[1],
            url=row[2],
            cursor=row[3],
        )

    async def find(self, driver: str, url: str) -> typing.Optional[FeedData]:
        cur = await self._connection.execute("""
            SELECT
                id,
                driver,
                url,
                cursor
            FROM
                feeds
            WHERE
                driver = ? AND url = ?
            LIMIT 1
        """, (driver, url))
        row = await cur.fetchone()
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
        cur = await self._connection.execute("""
            INSERT INTO
                feeds(driver, url)
            VALUES
                (?, ?)
        """, (driver, url))
        id = cur.lastrowid
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
                cursor = ?
            WHERE
                id = ?
        """, (cursor, id))
