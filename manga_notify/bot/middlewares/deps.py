import typing

from aiogram import BaseMiddleware
from aiogram import types

from ... import dependencies


class DependenciesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[
            [types.TelegramObject, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any]
        ],
        event: types.TelegramObject,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        data['deps'] = dependencies.get()
        return await handler(event, data)
