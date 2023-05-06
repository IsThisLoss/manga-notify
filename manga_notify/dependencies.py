import contextlib

import arq
import aiogram
import asyncpg

from . import settings
from . import database


class Dependencies:
    def __init__(self):
        self._cfg = None
        self._db_pool = None
        self._queues = None
        self._bot = None

    def get_cfg(self) -> settings.Settings:
        if not self._cfg:
            self._cfg = settings.get_config()
        assert self._cfg
        return self._cfg

    async def get_db_pool(self) -> asyncpg.Pool:
        if not self._db_pool:
            self._db_pool = await asyncpg.create_pool(self.get_cfg().pg_conn)
        assert self._db_pool
        return self._db_pool

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
        if not self._bot:
            cfg = self.get_cfg()
            self._bot = aiogram.Bot(cfg.tg_token)
        assert self._bot
        return self._bot

    @contextlib.asynccontextmanager
    async def get_db(self):
        pool = await self.get_db_pool()
        assert pool
        async with pool.acquire() as conn:
            yield database.database.DataBase(conn)


_deps = Dependencies()


def get() -> Dependencies:
    return _deps
