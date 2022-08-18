from aiogram import Bot
from aiogram.types import ParseMode

from .. import settings


# FIXME: import bot from ..bot
# create more objects than we need here,
# so create new bot
cfg = settings.get_config()
bot = Bot(cfg.tg_token)


async def job(_, user_id: str, message: str):
    await bot.send_message(chat_id=user_id, text=message, parse_mode=ParseMode.MARKDOWN)
