from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
import typing

from aiogram import types

from ..i18n import gettext as _
from . import callback_data
from .router import make_router
from .. import dependencies


# NOTE: Telegram API has max size of callback data
# It is 64 bytes, so use sortcuts
_TOMORROW_MORNING = 'TM'
_TOMORROW_EVENING = 'TE'
_SATURDAY_MORNING = 'SM'


def build_remind_keyboard() -> types.InlineKeyboardMarkup:
    keys = []
    method = callback_data.Methods.LATER_TIME
    buttons = (
        (_('Tomorrow at 09:00'), _TOMORROW_MORNING),
        (_('Tomorrow at 21:00'), _TOMORROW_EVENING),
        (_('Saturday at 09:00'), _SATURDAY_MORNING),
    )
    for text, when in buttons:
        keys.append(
            types.InlineKeyboardButton(
                text=text,
                callback_data=callback_data.CallbackData(
                    method=method,
                    payload={'when': when},
                ).serialize()
            ),
        )
    return types.InlineKeyboardMarkup(inline_keyboard=[keys])


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
    if when == _TOMORROW_MORNING:
        result = now + timedelta(days=1)
        return result.replace(hour=9, minute=0, second=0, microsecond=0)
    if when == _TOMORROW_EVENING:
        result = now + timedelta(days=1)
        return result.replace(hour=21, minute=0, second=0, microsecond=0)
    if when == _SATURDAY_MORNING:
        return find_next_saturday(now).replace(
            hour=9, minute=0, second=0, microsecond=0,
        )
    return None


async def button_callback(
    deps: dependencies.Dependencies,
    user_id: str,
    message_id: int,
    data: callback_data.CallbackData,
):
    now = datetime.now(ZoneInfo(deps.get_cfg().reminder_timezone))
    until = _get_queue_time(now, data.payload.get('when', ''))
    if not until:
        return False
    queues = await deps.get_queues()
    await queues.enqueue_job(
        'remind_later',
        user_id,
        message_id,
        _defer_until=until,
        _job_id=f'remind:{user_id}:{message_id}:{until.isoformat()}',
    )
    return True


router = make_router(__name__)


@router.callback_query(
    callback_data.create_matcher(callback_data.Methods.LATER),
)
async def show_times(
    query: types.CallbackQuery, deps: dependencies.Dependencies,
):
    if not isinstance(query.message, types.Message):
        await query.answer(_('Message unavailable'), show_alert=True)
        return
    keyboard = build_remind_keyboard()
    if query.message.reply_markup:
        for row in query.message.reply_markup.inline_keyboard:
            links = [button for button in row if button.url]
            if links:
                keyboard.inline_keyboard.append(links)
    await query.message.edit_reply_markup(reply_markup=keyboard)
    timezone = deps.get_cfg().reminder_timezone
    await query.answer(
        _('Reminder timezone: {timezone}').format(timezone=timezone),
        show_alert=True,
    )


@router.callback_query(
    callback_data.create_matcher(callback_data.Methods.LATER_TIME),
)
async def schedule_reminder(
    query: types.CallbackQuery,
    deps: dependencies.Dependencies,
    user_id: str,
):
    data = callback_data.parse(query.data or '')
    if not data or not isinstance(query.message, types.Message):
        await query.answer(_('Message unavailable'), show_alert=True)
        return
    try:
        scheduled = await button_callback(
            deps, user_id, query.message.message_id, data,
        )
    except Exception:
        logging.exception('Failed to schedule reminder')
        await query.answer(_('Could not schedule the reminder. Try again'),
                           show_alert=True)
        return
    if not scheduled:
        await query.answer(_('Unknown reminder time'), show_alert=True)
        return
    rows = []
    if query.message.reply_markup:
        for row in query.message.reply_markup.inline_keyboard:
            links = [button for button in row if button.url]
            if links:
                rows.append(links)
    keyboard = (
        types.InlineKeyboardMarkup(inline_keyboard=rows) if rows else None
    )
    await query.message.edit_reply_markup(reply_markup=keyboard)
    await query.answer(_('Reminder scheduled'))
