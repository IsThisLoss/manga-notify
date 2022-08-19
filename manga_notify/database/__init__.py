import contextlib

from . import database
from .. import settings

import aiosqlite


@contextlib.asynccontextmanager
async def get_database():
    connection = await aiosqlite.connect(settings.get_config().db_string)
    try:
        yield database.DataBase(connection)
        await connection.commit()
    finally:
        await connection.rollback()
        await connection.close()
