# manga-notify

[RU](docs/README_RU.md)

Simple python bot, that notifies about new manga chapters through Telegram.

## Quick Start

To setup your own instance of this application

- Install docker and docker-compose
- Take docker compose form [docker-compose.yaml](docs/deploy/docker-compose.yaml)
- Put your Bot's token as environment variables `TG_TOKEN` (probably .env file)
- Run `docker-compose up -d`

## Development

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
