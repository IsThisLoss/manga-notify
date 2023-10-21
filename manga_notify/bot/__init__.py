from aiogram import Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage

from . import auth
from . import callback_data
from . import info_builder
from . import mal_search
from . import remind_later
from .. import dependencies
from ..drivers import driver_factory
from ..feed_processing import subscription


def _make_help():
    msg = (
        '/help - выводит это сообщение\n'
        '/start - регистрирует пользователя\n'
        '/subscribe - подписывает пользователя на обновления\n'
        '/subscriptions - возвращает список активных подписок\n'
        '/unsubscribe - отписывает пользователя от обновлений\n'
        '/mal - поиск тайтлов MyAnimeList '
        '(или /mal [manga|anime] *название*)\n'
    )
    return msg.strip()


deps = dependencies.get()
router = Router()
router.message.middleware.register(auth.AuthMiddleware())


@router.message(commands='start')
async def start_handler(message: types.Message):
    if not message.from_user:
        await message.reply('Бот может работать только с пользователями')
        return

    async with deps.get_db() as db:
        res = await db.users.register(
            str(message.from_user.id),
            str(message.from_user.username),
        )

    if res is True:
        await message.reply('Вы успешно зарегистрированы!')
    else:
        await message.reply('Произошла ошибка при регистрации')


@router.message(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Отменено')


@router.message(commands='help')
async def help_handler(message: types.Message):
    await message.reply(_make_help())


@router.message(commands='subscriptions')
async def subscriptions_handler(message: types.Message):
    if not message.from_user:
        await message.reply('Бот может работать только с пользователями')
        return
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        feeds = await user_subscription.get_user_feeds(str(message.from_user.id))
    data = []
    for feed in feeds:
        data.append(info_builder.build_feed_info(feed))
    msg = 'Нет активных подписок'
    if data:
        data_str = '\n'.join(data)
        msg = f'Активные подписки:\n{data_str}'
    await message.reply(
        msg,
        ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


class NewSubscription(StatesGroup):
    url = State()


@router.message(commands='subscribe')
async def subscribe_handler(message: types.Message, state: FSMContext):
    await state.set_state(NewSubscription.url)
    await message.reply('Введи ссылку на фид')


@router.message(state=NewSubscription.url)
async def url_state(message: types.Message, state: FSMContext):
    factory = driver_factory.DriverFactory()
    url = message.text.strip()
    driver = factory.find_driver(url)
    await state.finish()
    if not driver:
        await message.reply('Кажется, я еще не умею обрабатывать такие ссылки')
        return
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        is_subscribed = await user_subscription.subscribe(
            str(message.from_id),
            driver,
            url,
        )
        if is_subscribed:
            await message.reply('Вы успешно подписаны')
            return
        await message.reply('Не удалось создать фид')


@router.message(commands='unsubscribe')
async def unsubscribe_hander(message: types.Message):
    chat_id = str(message.from_id)
    async with deps.get_db() as db:
        user_subscription = subscription.UserSubscription(db)
        feeds = await user_subscription.get_user_feeds(chat_id)

    if not feeds:
        await message.reply('Нет активных подписок')
        return

    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    for feed in feeds:
        data = callback_data.CallbackData(
            method=callback_data.Methods.UNSUBSCRIBE,
            payload={'id': feed.get_id()},
        )
        text = feed.get_title() or feed.get_url()
        keyboard_markup.add(types.InlineKeyboardButton(
            text,
            callback_data=data.serialize(),
        ))
    await message.reply(
        'Выбери фид от которого нужно отписаться',
        reply_markup=keyboard_markup
    )


@router.callback_query(
    callback_data.create_matcher(callback_data.Methods.UNSUBSCRIBE),
)
async def unsubscribe_callback(callback_query: types.CallbackQuery):
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
    await callback_query.message.edit_text(
        msg,
        reply_markup=types.InlineKeyboardMarkup(),
    )
    await callback_query.answer('Готово')


@router.callback_query(
    callback_data.create_matcher(callback_data.Methods.LATER)
)
async def later_callback(callback_query: types.CallbackQuery):
    data = callback_data.parse(callback_query.data)
    if not data:
        await callback_query.answer('Что-то пошло не так')
        return

    user_id = str(callback_query.from_user.id)
    message_id = callback_query.message.message_id

    await remind_later.button_callback(deps, user_id, message_id, data)

    await callback_query.answer('Готово')


class MalSearch(StatesGroup):
    query = State()


@router.message(commands='mal')
async def mal_handler(message: types.Message):
    args = message.get_args()

    if not args:
        await MalSearch.query.set()
        await message.reply('Введи название тайтла')
        return

    searcher = mal_search.MalSearch()
    msg = await searcher.quick_search(args)
    await message.reply(
        msg,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@router.message(state=MalSearch.query)
async def mal_search_query_state(message: types.Message, state: FSMContext):
    text = message.text.strip()
    await state.finish()

    searcher = mal_search.MalSearch()
    msg = await searcher.search(text)
    await message.reply(
        msg,
        parse_mode=types.ParseMode.MARKDOWN,
    )


async def start_polling():
    redis = await deps.get_redis()
    storage = RedisStorage(
        redis=redis,
    )
    bot = deps.get_bot()
    dp = Dispatcher(storage=storage)
    await dp.start_polling(bot)
