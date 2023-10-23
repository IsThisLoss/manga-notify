from aiogram import enums
from aiogram import types
from aiogram import filters
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from . import mal_search
from .router import make_router


router = make_router(__name__)


class MalSearch(StatesGroup):
    query = State()


@router.message(filters.Command('mal'))
async def mal_handler(message: types.Message, state: FSMContext):
    args = (message.text or '').split()

    if not args:
        await state.set_state(MalSearch.query)
        await message.reply('Введи название тайтла')
        return

    searcher = mal_search.MalSearch()
    msg = await searcher.quick_search(args[1])
    await message.reply(
        msg,
        parse_mode=enums.ParseMode.MARKDOWN,
    )


@router.message(filters.StateFilter(MalSearch.query))
async def mal_search_query_state(message: types.Message, state: FSMContext):
    text = (message.text or '').strip()
    await state.clear()

    searcher = mal_search.MalSearch()
    msg = await searcher.search(text)
    await message.reply(
        msg,
        parse_mode=enums.ParseMode.MARKDOWN,
    )
