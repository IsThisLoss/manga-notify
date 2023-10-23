from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from . import basic_commands, subscription_flow, mal_search_flow
from .. import dependencies


async def start_polling():
    deps = dependencies.get()
    redis = await deps.get_redis()
    storage = RedisStorage(
        redis=redis,
    )
    bot = deps.get_bot()
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        basic_commands.router,
        subscription_flow.router,
        mal_search_flow.router,
    )
    await dp.start_polling(bot)


async def start_webhook():
    pass
