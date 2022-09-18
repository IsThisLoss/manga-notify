from aiogram.types import ParseMode

# from ..bot import remind_later

from .. import dependencies


async def job(ctx, user_id: str, message: str):
    deps: dependencies.Dependencies = ctx['deps']
    bot = deps.get_bot()

    # TODO keyboard = remind_later.build_remind_keyboard()
    await bot.send_message(
        chat_id=user_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN,
    )
