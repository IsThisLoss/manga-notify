from datetime import datetime, timedelta
import typing

from aiogram import types

from . import callback_data
from .. import dependencies


# NOTE: Telegram API has max size of callback data
# It is 64 bytes, so use sortcuts
_TOMORROW_MOGRIN = 'TM'
_TOMORROW_EVENING = 'TE'
_SATURDAY_MORNING = 'SM'


def build_remind_keyboard() -> types.InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    method = callback_data.Methods.LATER
    buttons = (
        ('Завтра утром', _TOMORROW_MOGRIN),
        ('Завтра вечером', _TOMORROW_EVENING),
        ('В субботу утром', _SATURDAY_MORNING),
    )
    for text, when in buttons:
        keyboard_markup.add(
            types.InlineKeyboardButton(
                text,
                callback_data=callback_data.CallbackData(
                    method=method,
                    payload={'when': when},
                ).serialize()
            ),
        )
    return keyboard_markup


def find_next_saturday(now: datetime) -> datetime:
    saturday = 5
    weekday = now.weekday()
    if weekday < saturday:
        delta = saturday - now.weekday()
    elif weekday == saturday:
        delta = 7
    else:
        delta = 6
    return now + timedelta(days=delta)


def _get_queue_time(now: datetime, when: str) -> typing.Optional[datetime]:
    if when == _TOMORROW_MOGRIN:
        result = now + timedelta(days=1)
        return result.replace(hour=9, minute=0)
    if when == _TOMORROW_EVENING:
        result = now + timedelta(days=1)
        return result.replace(hour=21, minute=0)
    if when == _SATURDAY_MORNING:
        result = find_next_saturday(now).replace(hour=9, minute=0)
        return result
    return None


async def button_callback(
    deps: dependencies.Dependencies,
    user_id: str,
    message_id: int,
    data: callback_data.CallbackData,
):
    now = datetime.now()
    until = _get_queue_time(now, data.payload['when'])
    if not until:
        return False
    queues = await deps.get_queues()
    await queues.enqueue_job(
        'remind_later',
        user_id,
        message_id,
        _defer_until=until,
    )
    return True
