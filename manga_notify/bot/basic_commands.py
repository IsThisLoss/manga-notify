from aiogram import filters
from aiogram import types
from aiogram.fsm.context import FSMContext

from ..i18n import gettext as _
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
        await message.reply(_('You have been registered!'))
    else:
        await message.reply(_('Registration failed'))


@router.message(filters.Command('cancel'))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply(_('Cancelled'))


@router.message(filters.Command('help'))
async def help_handler(message: types.Message):
    msg = _(
        '/help - show this message\n'
        '/start - register a user\n'
        '/subscribe - subscribe to updates\n'
        '/subscriptions - list active subscriptions\n'
        '/unsubscribe - unsubscribe from updates\n'
        '/mal - search MyAnimeList titles (or /mal [manga|anime] *title*)\n'
    )
    msg = msg.strip()
    await message.reply(msg)
