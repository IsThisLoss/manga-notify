from aiogram import enums
from aiogram import filters
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import callback_data
from . import info_builder
from .. import dependencies
from ..drivers import driver_factory
from ..feed_processing import subscription
from .router import make_router


router = make_router(__name__)


class NewSubscription(StatesGroup):
    url = State()


@router.message(filters.Command('subscriptions'))
async def subscriptions_handler(
    message: types.Message,
    deps: dependencies.Dependencies,
    user_id: str,
):
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        feeds = await user_subscription.get_user_feeds(user_id)
    data = []
    for feed in feeds:
        data.append(info_builder.build_feed_info(feed))
    msg = 'Нет активных подписок'
    if data:
        data_str = '\n'.join(data)
        msg = f'Активные подписки:\n{data_str}'
    await message.reply(
        msg,
        enums.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@router.message(filters.Command('subscribe'))
async def subscribe_handler(message: types.Message, state: FSMContext):
    await state.set_state(NewSubscription.url)
    await message.reply('Введи ссылку на фид')


@router.message(filters.StateFilter(NewSubscription.url))
async def url_state(
    message: types.Message,
    state: FSMContext,
    deps: dependencies.Dependencies,
    user_id: str
):
    factory = driver_factory.DriverFactory()
    url = (message.text or '').strip()
    driver = factory.find_driver(url)
    await state.clear()

    if not driver:
        await message.reply('Кажется, я еще не умею обрабатывать такие ссылки')
        return

    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        is_subscribed = await user_subscription.subscribe(
            str(user_id),
            driver,
            url,
        )
        if is_subscribed:
            await message.reply('Вы успешно подписаны')
            return
        await message.reply('Не удалось создать фид')


@router.message(filters.Command('unsubscribe'))
async def unsubscribe_hander(
    message: types.Message,
    deps: dependencies.Dependencies,
    user_id: str
):
    chat_id = str(user_id)
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        feeds = await user_subscription.get_user_feeds(chat_id)

    if not feeds:
        await message.reply('Нет активных подписок')
        return

    buttons = []
    for feed in feeds:
        data = callback_data.CallbackData(
            method=callback_data.Methods.UNSUBSCRIBE,
            payload={'id': feed.get_id()},
        )
        text = feed.get_title() or feed.get_url()
        buttons.append(types.InlineKeyboardButton(
            text=text,
            callback_data=data.serialize(),
        ))
    keyboard_markup = types.InlineKeyboardMarkup(inline_keyboard=[buttons])
    await message.reply(
        'Выбери фид от которого нужно отписаться',
        reply_markup=keyboard_markup
    )


@router.callback_query(
    callback_data.create_matcher(callback_data.Methods.UNSUBSCRIBE),
)
async def unsubscribe_callback(
    callback_query: types.CallbackQuery,
    deps: dependencies.Dependencies,
    user_id: str,
):
    data = callback_data.parse(callback_query.data)
    if not data:
        await callback_query.answer('Что-то пошло не так')
        return

    feed_id = data.payload['id']
    await callback_query.answer('Готово')
    user_id = str(callback_query.from_user.id)

    msg = 'Не удалось найти фид'
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        is_unsubscribed = await user_subscription.unsubscribe(
            user_id,
            feed_id,
        )
        if is_unsubscribed:
            msg = 'Вы успешно отписаны'
    if callback_query.message:
        await callback_query.message.edit_text(
            msg,
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[]),
        )
    await callback_query.answer('Готово')
