import contextlib

from . import database
from .. import settings

import asyncpg


_pool = None


@contextlib.asynccontextmanager
async def get_database():
    global _pool

    cfg = settings.get_config()
    if not _pool:
        _pool = await asyncpg.create_pool(cfg.pg_conn)

    async with _pool.acquire() as conn:
        yield database.DataBase(conn)
