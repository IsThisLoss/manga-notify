import contextlib

from . import database
from .. import settings

import aiosqlite


@contextlib.asynccontextmanager
async def get_database():
    connection = await aiosqlite.connect(settings.get_config().db_string)
    try:
        yield database.DataBase(connection)
    finally:
        await connection.close()
