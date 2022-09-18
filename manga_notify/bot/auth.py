import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from .. import dependencies


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, _: dict):
        if message.get_command() == '/start':
            return

        deps = dependencies.get()

        user_id = str(message.from_id)
        async with deps.get_db() as db:
            if await db.users.exists(user_id):
                return

        logging.info(f'User {user_id} was not found')
        await message.reply(
            'Прежде чем использовать бота нужно вызвать /start'
        )
        raise CancelHandler()
