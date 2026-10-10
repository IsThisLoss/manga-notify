from aiogram import Router
from aiogram.utils.i18n import ConstI18nMiddleware

from ..i18n import i18n

from .middlewares import auth
from .middlewares import deps


def make_router(name: str) -> Router:
    router = Router(name=name)
    ConstI18nMiddleware(locale=i18n.default_locale, i18n=i18n).setup(router)
    router.message.middleware.register(deps.DependenciesMiddleware())
    router.message.middleware.register(auth.AuthMessageMiddleware())
    router.callback_query.middleware.register(deps.DependenciesMiddleware())
    router.callback_query.middleware.register(auth.AuthCallbackMiddleware())
    return router
