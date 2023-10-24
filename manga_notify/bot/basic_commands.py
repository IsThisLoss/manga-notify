
from aiogram import filters
from aiogram import types
from aiogram.fsm.context import FSMContext

from .. import dependencies
from .router import make_router


router = make_router(__name__)


@router.message(filters.Command('start'))
async def start_handler(
    message: types.Message,
    deps: dependencies.Dependencies,
    user_id: str,
    login: str,
):
    db = await deps.get_db()
    res = await db.users.register(user_id, login)

    if res is True:
        await message.reply('Вы успешно зарегистрированы!')
    else:
        await message.reply('Произошла ошибка при регистрации')


@router.message(filters.Command('cancel'))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Отменено')


@router.message(filters.Command('help'))
async def help_handler(message: types.Message):
    msg = (
        '/help - выводит это сообщение\n'
        '/start - регистрирует пользователя\n'
        '/subscribe - подписывает пользователя на обновления\n'
        '/subscriptions - возвращает список активных подписок\n'
        '/unsubscribe - отписывает пользователя от обновлений\n'
        '/mal - поиск тайтлов MyAnimeList '
        '(или /mal [manga|anime] *название*)\n'
    )
    msg = msg.strip()
    await message.reply(msg)
