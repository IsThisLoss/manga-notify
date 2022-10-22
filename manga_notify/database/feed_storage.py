import typing

import asyncpg


class FeedType:
    Anime = 'anime'
    Manga = 'manga'


class FeedData:
    def __init__(
            self,
            id,
            driver,
            url,
            cursor,
            title=None,
            mal_url=None,
    ):
        self._id = id
        self._driver = driver
        self._url = url
        self._cursor = cursor
        self._title = title
        self._mal_url = mal_url

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

    def get_title(self) -> typing.Optional[str]:
        return self._title

    def set_title(self, title: str):
        self._title = title

    def get_mal_url(self) -> typing.Optional[str]:
        return self._mal_url

    def set_mal_url(self, mal_url: str):
        self._mal_url = mal_url


class FeedStorage:
    def __init__(self, conn: asyncpg.Connection):
        self._connection = conn

    async def get_all(self) -> typing.List[FeedData]:
        rows = await self._connection.fetch("""
            SELECT
                id, driver, url, cursor, title, mal_url
            FROM
                feeds
        """)
        result = []
        for id, driver, url, cursor, title, mal_url in rows:
            data = FeedData(
                id=id,
                driver=driver,
                url=url,
                cursor=cursor,
                title=title,
                mal_url=mal_url,
            )
            result.append(data)
        return result

    async def get(self, id: int) -> typing.Optional[FeedData]:
        row = await self._connection.fetchrow("""
            SELECT
                id, driver, url, cursor, title, mal_url
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
            title=row[4],
            mal_url=row[5],
        )

    async def find(self, driver: str, url: str) -> typing.Optional[FeedData]:
        row = await self._connection.fetchrow("""
            SELECT
                id,
                driver,
                url,
                cursor,
                title,
                mal_url
            FROM
                feeds
            WHERE
                driver = $1 AND url = $2
            LIMIT 1
        """, driver, url)
        if not row:
            return None
        id, driver, url, cursor, title, mal_url = row
        return FeedData(
            id=id,
            driver=driver,
            url=url,
            cursor=cursor,
            title=title,
            mal_url=mal_url,
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

    async def find_without_mal_link(
        self,
        limit: int = 10,
    ) -> typing.List[FeedData]:
        rows = await self._connection.fetch("""
            SELECT
                id, driver, url, cursor, title, mal_url
            FROM
                feeds
            WHERE
                title IS NOT NULL
                AND
                mal_url IS NULL
            LIMIT $1
        """, limit)
        result = []
        for id, driver, url, cursor, title, mal_url in rows:
            data = FeedData(
                id=id,
                driver=driver,
                url=url,
                cursor=cursor,
                title=title,
                mal_url=mal_url,
            )
            result.append(data)
        return result

    async def update(
        self,
        id: int,
        cursor: str,
        title: typing.Optional[str],
    ):
        query = """
            UPDATE
                feeds
            SET
                cursor = $2,
                title = $3
            WHERE
                id = $1
        """
        await self._connection.execute(
            query,
            id,
            cursor,
            title,
        )

    async def update_mal_url(
        self,
        id: int,
        mal_url: str,
    ):
        query = """
            UPDATE
                feeds
            SET
                mal_url = $2
            WHERE
                id = $1
        """
        await self._connection.execute(
            query,
            id,
            mal_url,
        )
