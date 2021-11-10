# manga-notify

[RU](docs/README_RU.md)

Simple python bot, that notifies about new manga chapters through Telegram.

## Quick Start

To setup your own instance of this application

- Install docker and docker-compose
- Take docker compose form [docker-compose.yaml](docs/deploy/docker-compose.yaml)
- Put your Bot's token as environment variables `TG_TOKEN` (probably .env file)
- And run `docker-compose up -d`

## Development

To setup development environment use standart flow to venv

```bash
python3 -m virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

All settings stored as environment variables, to set them up
use .env file. To development mandatory settings is

- `TG_TOKEN` is bot's Telegram token
- `DB_STRING` is path to sqlite database file
- `PARSING_INTERVAL` is interval in minutes to run background parsing

To start application execute

```bash
python -m manga_notify.main
```
