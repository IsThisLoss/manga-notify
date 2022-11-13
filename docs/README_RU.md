# manga-notify

Простой телеграм бот, который отправляет сообщение о новых главах через Telegram.

## Быстрый старт

Чтобы запустить свой собственный экзампляр бота нужно

- Установить docker и docker-compose
- Взять docker-compose файл из [docker-compose.yaml](deploy/docker-compose.yaml)
- Положить токен бота в переменную окружения `TG_TOKEN` (возможно через файл .env)
- Запустить `docker-compose up -d`

## Разработка

Разработческое окружение настраивается стандартным для virtualenv способом.

```bash
python3 -m virtualenv venv
. ./venv/bin/activate
pip install -e ".[dev,test]"
```

Все настройки приложения задаются через переменные окружения. Для разработки обязательные параметр.

- `TG_TOKEN` - токен телеграм бота
- `PARSING_INTERVAL` - интервал фонового парсинга в минутах 

А так же для разработке нужны postres и redis.
Их можно запустить выполнив

`make start-dev-env`

Остановить их

`down-dev-env`

Чтобы запустить бота нужно выполнить

`make run-bot`

Чтобы запустить фоновые процессы, например парсинг фидов, нужно выполнить

`make run-jobs`

Перед созданием PR рекомендуется запустить локально тесты

```bash
make flake8-check
make mypy-check
make tests
```
