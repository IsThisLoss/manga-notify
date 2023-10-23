# mypy: disable-error-code="override"

import logging
import typing

from aiogram import BaseMiddleware
from aiogram import types

from ... import dependencies


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[
            [types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any]
        ],
        event: types.Message,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        if not event.from_user:
            await event.reply('Я умею работать только с пользователями')
            return

        user_id = str(event.from_user.id)
        login = str(event.from_user.username)

        data['user_id'] = user_id
        data['login'] = login

        if (event.text or '').strip() == '/start':
            return await handler(event, data)

        deps: dependencies.Dependencies = data['deps']

        async with deps.get_db() as db:
            user_exists = await db.users.exists(user_id)
            if not user_exists:
                logging.info(f'User {user_id} was not found')
                await event.reply(
                    'Прежде чем использовать бота нужно вызвать /start'
                )
                return
        return await handler(event, data)
