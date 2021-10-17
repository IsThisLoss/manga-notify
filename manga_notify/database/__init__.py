from . import database
from .. import settings


def get_database():
    db_string = settings.get_config().db_string
    return database.DataBase(db_string)
