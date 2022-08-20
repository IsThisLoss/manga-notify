import logging

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from ..database import get_database


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, _: dict):
        if message.get_command() == '/start':
            return

        user_id = str(message.from_id)
        async with get_database() as db:
            if await db.users.exists(user_id):
                return

        logging.info(f'User {user_id} was not found')
        await message.reply(
            'Прежде чем использовать бота нужно вызвать /start'
        )
        raise CancelHandler()
