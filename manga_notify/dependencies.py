import aiogram
import aiohttp
import arq
import asyncpg

from redis.asyncio.client import Redis

from . import settings
from . import database


class Dependencies:
    def __init__(self):
        self._cfg = settings.get_config()
        self._bot = aiogram.Bot(self._cfg.tg_token)

        self._http_client = None
        self._db_pool = None
        self._redis = None
        self._queues = None

    async def _on_startup(self):
        await self.get_db_pool()
        await self.get_redis()
        await self.get_queues()
        await self.get_http_client()

    async def _on_shutdown(self):
        if self._http_client:
            await self._http_client.close()
        if self._queues:
            await self._queues.close()
        if self._db_pool:
            await self._db_pool.close()

    def get_cfg(self) -> settings.Settings:
        assert self._cfg
        return self._cfg

    async def get_db_pool(self) -> asyncpg.Pool:
        if not self._db_pool:
            cfg = self.get_cfg()
            self._db_pool = await asyncpg.create_pool(cfg.pg_conn)

        assert self._db_pool
        return self._db_pool

    async def get_redis(self) -> Redis:
        if not self._redis:
            cfg = self.get_cfg()
            self._redis = Redis(
                host=cfg.redis_host,
                port=cfg.redis_port,
                password=cfg.redis_password,
            )
            await self._redis.ping()
        return self._redis

    async def get_queues(self) -> arq.connections.ArqRedis:
        if not self._queues:
            cfg = self.get_cfg()
            redis_settings = arq.connections.RedisSettings(
                host=cfg.redis_host,
                port=cfg.redis_port,
                password=cfg.redis_password,
            )
            self._queues = await arq.create_pool(redis_settings)

        assert self._queues
        return self._queues

    def get_bot(self) -> aiogram.Bot:
        assert self._bot
        return self._bot

    async def get_db(self):
        pool = await self.get_db_pool()
        assert pool
        return database.database.DataBase(pool)

    async def get_http_client(self) -> aiohttp.ClientSession:
        if not self._http_client:
            self._http_client = aiohttp.ClientSession(
                raise_for_status=True,
                timeout=aiohttp.ClientTimeout(
                    total=self._cfg.http_client_timeout,
                ),
            )
        assert self._http_client
        return self._http_client


_deps = Dependencies()


def get() -> Dependencies:
    return _deps


async def on_startup():
    await _deps._on_startup()


async def on_shutdown():
    await _deps._on_shutdown()
