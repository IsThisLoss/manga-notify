from aiogram import types

# from ..bot import remind_later

from .. import dependencies


def build_mal_keyboard(mal_url: str):
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(
        types.InlineKeyboardButton(
            'MyAnimeList',
            url=mal_url,
        )
    )
    return keyboard_markup


async def job(ctx, user_id: str, message: str, extra: dict):
    deps: dependencies.Dependencies = ctx['deps']
    bot = deps.get_bot()

    keyboard = None
    mal_url = extra.get('mal_url')
    if mal_url:
        keyboard = build_mal_keyboard(mal_url)
    await bot.send_message(
        chat_id=user_id,
        text=message,
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )
