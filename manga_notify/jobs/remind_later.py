from aiogram import Bot

from .. import settings


# FIXME: import bot from ..bot
# create more objects than we need here,
# so create new bot
cfg = settings.get_config()
bot = Bot(cfg.tg_token)


async def job(_, user_id: str, message_id: int):
    await bot.send_message(
        user_id,
        'Напоминаю',
        reply_to_message_id=message_id
    )
