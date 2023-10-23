# mypy: disable-error-code="override"

import logging
import typing

from aiogram import BaseMiddleware
from aiogram import types

from ... import dependencies


class AuthMiddleware(BaseMiddleware):
    async def on_empty_user(self, message: types.Message):
        await message.reply('Я умею работать только с пользователями')

    async def on_not_found_user(self, message: types.Message):
        await message.reply(
            'Прежде чем использовать бота нужно вызвать /start'
        )

    async def user_exists(
        self,
        deps: dependencies.Dependencies,
        user_id: str,
    ) -> bool:
        async with deps.get_db() as db:
            user_exists = await db.users.exists(user_id)
            if not user_exists:
                logging.info(f'User {user_id} was not found')
                return False
        return True


class AuthMessageMiddleware(AuthMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[
            [types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any]
        ],
        event: types.Message,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        deps: dependencies.Dependencies = data['deps']

        if not event.from_user:
            await self.on_empty_user(event)
            return

        user_id = str(event.from_user.id)
        login = str(event.from_user.username)

        data['user_id'] = user_id
        data['login'] = login

        if (event.text or '').strip() == '/start':
            return await handler(event, data)

        if not await self.user_exists(deps, user_id):
            await self.on_not_found_user(event)
            return

        return await handler(event, data)


class AuthCallbackMiddleware(AuthMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[
            [types.CallbackQuery, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any]
        ],
        event: types.CallbackQuery,
        data: typing.Dict[str, typing.Any]
    ) -> typing.Any:
        deps: dependencies.Dependencies = data['deps']
        event.message

        if not event.from_user:
            if event.message:
                await self.on_empty_user(event.message)
            return

        user_id = str(event.from_user.id)
        login = str(event.from_user.username)

        data['user_id'] = user_id
        data['login'] = login

        if not await self.user_exists(deps, user_id):
            if event.message:
                await self.on_not_found_user(event.message)
            return

        return await handler(event, data)
