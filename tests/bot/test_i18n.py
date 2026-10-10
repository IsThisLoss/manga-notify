import ast
from pathlib import Path
from string import Formatter
from unittest.mock import AsyncMock

from aiogram.utils.i18n import ConstI18nMiddleware
from babel.messages.extract import extract_from_dir
from babel.messages.pofile import read_po
import pytest

from manga_notify.i18n import gettext as _, i18n
from manga_notify.bot import basic_commands
from manga_notify.bot.router import make_router
from manga_notify.drivers.driver import ParsingItem
from manga_notify.feed_processing.feed_message import FeedMessage


@pytest.mark.asyncio
async def test_handler_and_worker_default_to_russian_without_context():
    message = AsyncMock()
    await basic_commands.help_handler(message)
    assert '/subscribe - подписывает' in message.reply.call_args.args[0]
    release = FeedMessage(
        [ParsingItem(name='Chapter 1', link='https://a')], None,
    )
    assert release.serialize() == 'Новый выпуск [Chapter 1](https://a)'
    assert _('Reminder') == 'Напоминаю'


@pytest.mark.asyncio
async def test_middleware_wraps_auth_and_handlers():
    router = make_router('i18n-test')
    for observer in (router.message, router.callback_query):
        middleware = next(
            item for item in observer.outer_middleware
            if isinstance(item, ConstI18nMiddleware)
        )
        handler = AsyncMock(side_effect=lambda event, data: _('Cancelled'))
        # An unrelated ambient locale must not change this bot's language.
        with i18n.use_locale('en'):
            assert await middleware(handler, None, {}) == 'Отменено'
            assert i18n.current_locale == 'en'
    assert i18n.current_locale == 'ru'


def test_catalog_covers_all_messages_and_placeholders():
    root = Path(__file__).resolve().parents[2] / 'manga_notify'
    with (root / 'locales/ru/LC_MESSAGES/messages.po').open('rb') as stream:
        catalog = read_po(stream)
    extracted = list(extract_from_dir(str(root)))
    assert extracted
    for filename, line, msgid, comments, context in extracted:
        entry = catalog.get(msgid)
        assert entry is not None, (filename, line, msgid)
        assert entry.string
        assert i18n.gettext(msgid) == entry.string
        fields = lambda text: {  # noqa: E731
            field for _, field, _, _ in Formatter().parse(text)
            if field is not None
        }
        assert fields(msgid) == fields(entry.string)


def test_translation_calls_use_literal_templates():
    root = Path(__file__).resolve().parents[2] / 'manga_notify'
    for path in root.rglob('*.py'):
        for node in ast.walk(ast.parse(path.read_text())):
            if (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Name)
                    and node.func.id == '_'):
                assert isinstance(node.args[0], ast.Constant), path
