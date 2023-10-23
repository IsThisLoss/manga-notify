from aiogram import Router

from .middlewares import auth
from .middlewares import deps


def make_router(name: str) -> Router:
    router = Router(name=name)
    router.message.middleware.register(deps.DependenciesMiddleware())
    router.message.middleware.register(auth.AuthMiddleware())
    return router
