from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook import aiohttp_server
from aiohttp import web
import aiogram

from . import basic_commands, subscription_flow, mal_search_flow
from .. import dependencies


async def _make_dispatcher(deps: dependencies.Dependencies) -> Dispatcher:
    redis = await deps.get_redis()
    storage = RedisStorage(
        redis=redis,
    )
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        basic_commands.router,
        subscription_flow.router,
        mal_search_flow.router,
    )
    return dp


async def start_polling():
    deps = dependencies.get()
    dp = await _make_dispatcher(deps)
    bot = deps.get_bot()
    await dp.start_polling(bot)


async def on_startup(bot: aiogram.Bot) -> None:
    deps = dependencies.get()
    cfg = deps.get_cfg()
    await bot.set_webhook(
        f'{cfg.base_webhook_url}{cfg.webhook_path}',
        secret_token=cfg.webhook_secret,
    )


async def start_webhook():
    deps = dependencies.get()
    cfg = deps.get_cfg()

    dp = await _make_dispatcher(deps)
    bot = deps.get_bot()

    app = web.Application()
    webhook_requests_handler = aiohttp_server.SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=cfg.webhook_secret,
    )
    webhook_requests_handler.register(app, path=cfg.webhook_path)
    aiohttp_server.setup_application(app, dp, bot=bot)

    web.run_app(app, host='127.0.0.1', port=cfg.web_server_port)
