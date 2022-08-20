from aiogram import Bot, types
from aiogram.types import ParseMode

from .. import settings
from ..bot import callback_data


# FIXME: import bot from ..bot
# create more objects than we need here,
# so create new bot
cfg = settings.get_config()
bot = Bot(cfg.tg_token)


async def job(_, user_id: str, message: str):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(
        types.InlineKeyboardButton(
            'Завтра утром',
            callback_data=callback_data.CallbackData(
                method='feed_notify',
                payload={'when': 'morning'},
            ).serialize()
        ),
        types.InlineKeyboardButton(
            'Завтра вечером',
            callback_data=callback_data.CallbackData(
                method='feed_notify',
                payload={'when': 'morning'},
            ).serialize()
        ),
    )

    await bot.send_message(
        chat_id=user_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN,
    )
