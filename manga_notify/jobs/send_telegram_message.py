from aiogram import enums
from aiogram import types

from ..bot import callback_data

from .. import dependencies


def build_mal_keyboard(
    mal_url: str,
) -> types.InlineKeyboardMarkup:
    buttons = []
    buttons.append(
        types.InlineKeyboardButton(
            text='MyAnimeList',
            url=mal_url,
        )
    )
    return types.InlineKeyboardMarkup(inline_keyboard=[buttons])


async def job(ctx, user_id: str, message: str, extra: dict):
    deps: dependencies.Dependencies = ctx['deps']
    bot = deps.get_bot()

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text='Напомнить позже',
            callback_data=callback_data.CallbackData(
                method=callback_data.Methods.LATER, payload={},
            ).serialize(),
        ),
    ]])
    mal_url = extra.get('mal_url')
    if mal_url:
        keyboard.inline_keyboard.extend(
            build_mal_keyboard(mal_url).inline_keyboard,
        )
    await bot.send_message(
        chat_id=user_id,
        text=message,
        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )
