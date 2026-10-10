from datetime import datetime

import pytest

from manga_notify.bot import remind_later


@pytest.mark.parametrize(
    'now, expected',
    (
        pytest.param(
            '2022-09-12',
            '2022-09-17',
            id='monday',
        ),
        pytest.param(
            '2022-09-13',
            '2022-09-17',
            id='tuesday',
        ),
        pytest.param(
            '2022-09-14',
            '2022-09-17',
            id='wednesday',
        ),
        pytest.param(
            '2022-09-15',
            '2022-09-17',
            id='thursday',
        ),
        pytest.param(
            '2022-09-16',
            '2022-09-17',
            id='friday',
        ),
        pytest.param(
            '2022-09-17',
            '2022-09-24',
            id='saturday',
        ),
        pytest.param(
            '2022-09-18',
            '2022-09-24',
            id='sunday',
        ),
    )
)
def test_find_next_saturday(now, expected):
    now_dt = datetime.strptime(now, '%Y-%m-%d')
    result = remind_later.find_next_saturday(now_dt)
    assert result.strftime('%Y-%m-%d') == expected


@pytest.mark.parametrize('when,hour,day', [
    ('TM', 9, 13), ('TE', 21, 13), ('SM', 9, 17),
])
def test_queue_time(when, hour, day):
    from zoneinfo import ZoneInfo

    now = datetime(2022, 9, 12, 23, 59, 42, 123, ZoneInfo('Europe/Moscow'))
    result = remind_later._get_queue_time(now, when)
    assert result == datetime(2022, 9, day, hour, tzinfo=now.tzinfo)
    assert result > now


@pytest.mark.asyncio
async def test_enqueue_reminder():
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, Mock
    from manga_notify.bot import callback_data

    queue = SimpleNamespace(enqueue_job=AsyncMock())
    deps = SimpleNamespace(
        get_cfg=Mock(return_value=SimpleNamespace(
            reminder_timezone='Europe/Moscow',
        )),
        get_queues=AsyncMock(return_value=queue),
    )
    data = callback_data.CallbackData(
        method='LATER_TIME', payload={'when': 'TM'},
    )
    assert await remind_later.button_callback(deps, '1', 42, data)
    assert await remind_later.button_callback(deps, '1', 42, data)
    first, second = queue.enqueue_job.call_args_list
    # Stable job ID prevents duplicate pending reminders.
    assert first == second
    assert first.args == ('remind_later', '1', 42)
    until = first.kwargs['_defer_until']
    assert until.hour == 9
    assert str(until.tzinfo) == 'Europe/Moscow'
    assert until.second == until.microsecond == 0
    data.payload = {'when': 'invalid'}
    assert not await remind_later.button_callback(deps, '1', 42, data)
    assert queue.enqueue_job.call_count == 2


@pytest.mark.asyncio
@pytest.mark.parametrize('mal_url', [None, 'https://myanimelist.net/manga/1'])
async def test_notification_and_time_menu(mal_url):
    from types import SimpleNamespace
    from unittest.mock import AsyncMock
    from aiogram import types
    from manga_notify.bot import callback_data
    from manga_notify.jobs import send_telegram_message

    bot = SimpleNamespace(send_message=AsyncMock())
    deps = SimpleNamespace(
        get_bot=lambda: bot,
        get_cfg=lambda: SimpleNamespace(reminder_timezone='Europe/Moscow'),
    )
    await send_telegram_message.job(
        {'deps': deps}, '1', 'Новый выпуск', {'mal_url': mal_url},
    )
    keyboard = bot.send_message.call_args.kwargs['reply_markup']
    data = callback_data.parse(keyboard.inline_keyboard[0][0].callback_data)
    assert data.method == callback_data.Methods.LATER
    message = types.Message(
        message_id=42, date=datetime.now(),
        chat=types.Chat(id=1, type='private'), reply_markup=keyboard,
    )
    query = SimpleNamespace(message=message, answer=AsyncMock())
    edit = AsyncMock()
    from unittest.mock import patch
    with patch.object(types.Message, 'edit_reply_markup', edit):
        await remind_later.show_times(query, deps)
    menu = edit.call_args.kwargs['reply_markup']
    choices = menu.inline_keyboard[0]
    assert len(choices) == 3
    for button in choices:
        assert len(button.callback_data.encode()) <= 64
        data = callback_data.parse(button.callback_data)
        assert data.method == callback_data.Methods.LATER_TIME
    if mal_url:
        assert menu.inline_keyboard[-1][0].url == mal_url
    query.message = message.model_copy(update={'reply_markup': menu})
    query.data = choices[0].callback_data
    with patch.object(
        remind_later, 'button_callback', AsyncMock(),
    ) as schedule, patch.object(types.Message, 'edit_reply_markup', edit):
        await remind_later.schedule_reminder(query, deps, '1')
    assert schedule.call_args.args[1:3] == ('1', 42)
    query.answer.assert_called_with('Напоминание установлено')
    remaining = edit.call_args.kwargs['reply_markup']
    if mal_url:
        assert len(remaining.inline_keyboard) == 1
        assert remaining.inline_keyboard[0][0].url == mal_url
    else:
        assert remaining is None


@pytest.mark.asyncio
async def test_reminder_delivery_allows_deleted_original():
    from types import SimpleNamespace
    from unittest.mock import AsyncMock
    from manga_notify.jobs import remind_later as reminder_job

    bot = SimpleNamespace(send_message=AsyncMock())
    await reminder_job.job(
        {'deps': SimpleNamespace(get_bot=lambda: bot)}, '1', 42,
    )
    args = bot.send_message.call_args
    assert args.args == ('1', 'Напоминаю')
    assert args.kwargs['reply_parameters'].message_id == 42
    assert args.kwargs['reply_parameters'].allow_sending_without_reply


@pytest.mark.asyncio
async def test_queue_failure_is_reported():
    from types import SimpleNamespace
    from unittest.mock import AsyncMock, patch
    from aiogram import types
    from manga_notify.bot import callback_data

    query = SimpleNamespace(
        message=types.Message(
            message_id=42, date=datetime.now(),
            chat=types.Chat(id=1, type='private'),
        ),
        data=callback_data.CallbackData(
            method='LATER_TIME', payload={'when': 'TM'},
        ).serialize(),
        answer=AsyncMock(),
    )
    with patch.object(
        remind_later, 'button_callback',
        AsyncMock(side_effect=ConnectionError('Redis unavailable')),
    ):
        await remind_later.schedule_reminder(query, None, '1')
    query.answer.assert_awaited_once_with(
        'Не удалось создать напоминание. Попробуй еще раз', show_alert=True,
    )
