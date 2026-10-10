# manga-notify

[RU](docs/README_RU.md)

Simple python bot, that notifies about new manga chapters through Telegram.

## Quick Start

To setup your own instance of this application

- Install Docker with the Compose plugin.
- Copy the files from [docs/deploy](docs/deploy) into the deployment directory,
  including `migrations/` and `supervisord.conf`.
- Copy `.env.example` to `.env`, set the Telegram token, release `TAG`, random
  passwords and webhook URL/secret. Keep `.env` private (`chmod 600 .env`).
- Configure an HTTPS reverse proxy to `127.0.0.1:8080` for the webhook path.
- Run `docker compose up -d --wait`.

Postgres and Redis run in the same Compose project, with data under `./volumes/`.
The SQL files initialize the schema only when Postgres starts with an empty data
folder; later schema changes require explicit migrations.

Production runs in `/home/manga-notify/app` on `sakura.isthisloss.ru`, under the
`manga-notify` user. GitHub tag releases copy deployment configuration and run
`deploy.sh` there. The `yc-deploy` GitHub environment stores the SSH `KEY`.
The webhook is `https://sakura.isthisloss.ru/webhook/sakura`.

## Development

Python 3.10 or newer is required.

To setup development environment use standart flow for venv

```bash
python3 -m virtualenv venv
. ./venv/bin/activate
pip install -e ".[dev,test]"
```

All settings stored as environment variables, to set them up
use .env file. To development mandatory settings is

- `TG_TOKEN` is bot's Telegram token
- `PARSING_INTERVAL` is interval in minutes to run background parsing

Also for development running instances of postgres and redis are required.
To start them one may run

`make start-dev-env`

To stop them

`make down-dev-env`

To start Telegram bot one needs to run

`make run-bot`

To run background processes, for example feeds parsing, one needs to run

`make run-jobs`

Before submiting a PR, it is recommended to run tests localy

```bash
make flake8-check
make mypy-check
make tests
```

## Reminders

Release notifications have a “Напомнить позже” button. Choose tomorrow at
09:00, tomorrow at 21:00, or next Saturday at 09:00. Saturday selected on a
Saturday means the following week. Times use `REMINDER_TIMEZONE` (default:
`Europe/Moscow`), independently of the server timezone. The bot confirms when
it has scheduled a reminder and removes the time selection buttons, preserving
the MyAnimeList link. The background worker must be running to deliver reminders. Reminders reply
to the release notification, or arrive separately if it has been deleted.

## Translations

User-facing messages use aiogram's `I18n`/gettext engine in
`manga_notify/i18n.py`. English message templates are marked with `_()`; Russian
translations live in `manga_notify/locales/ru/LC_MESSAGES/messages.po`.
The bot uses `ConstI18nMiddleware` with Russian as the default language, keeping
command replies, authentication messages, release notifications and reminders
consistent. Workers use the same engine without requiring a Telegram update.

When changing messages:

```bash
make locales-update
# Edit the Russian .po file and resolve any fuzzy entries.
make locales-compile
```

Commit the `.pot`, `.po` and compiled `.mo` files together. Catalogs are included
in the Python package and Docker image, so production does not need to compile
them at startup. Use literal templates such as `_("Hello, {name}").format(...)`;
format variables after translation rather than passing f-strings to `_()`.
