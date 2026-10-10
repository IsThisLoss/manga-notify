from pathlib import Path

from aiogram.utils.i18n import I18n


# Bind the engine so workers and standalone builders also have a locale
# without a Telegram update and middleware context.
i18n = I18n(
    path=Path(__file__).parent / 'locales',
    default_locale='ru',
    domain='messages',
)
gettext = i18n.gettext
