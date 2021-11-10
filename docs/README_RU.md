# manga-notify

Простой телеграм бот, который отправляет сообщение о новых главах через Telegram.

## Quick Start

## Development

Разработческое окружение настраивается стандартным для virtualenv способом.

```bash
python3 -m virtualenv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Все настройки приложения задаются через переменные окружения. Для разработки обязательные параметры 

`TG_TOKEN` - токен телеграм бота
`DB_STRING` - путь к sqlite базе данных 
`PARSING_INTERVAL` - интервал фонового парсинга в минутах 

Чтобы запустить приложение, нужно выполнить

```bash
python -m manga_notify.main
```
