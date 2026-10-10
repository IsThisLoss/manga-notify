from aiogram import types

from .. import dependencies


async def job(ctx, user_id: str, message_id: int):
    deps: dependencies.Dependencies = ctx['deps']
    bot = deps.get_bot()
    await bot.send_message(
        user_id,
        'Напоминаю',
        reply_parameters=types.ReplyParameters(
            message_id=message_id, allow_sending_without_reply=True,
        ),
    )
