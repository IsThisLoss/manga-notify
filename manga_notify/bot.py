import dataclasses
import typing

import telegram
import telegram.ext

from .database import get_database
from .drivers import driver_factory
from .feed_processing import subscription

from . import tg_utils


def _make_help():
    msg = (
        "/help выводит это сообщение\n"
        "/start регистрирует пользователя\n"
        "/drivers возвращает список доступных драйверов\n"
        "/subscribe [driver] [url] подписывает пользователя на обновления\n"
        "driver - один из доступных драйверов см. /drivers\n"
        "url - ссылка на feed для парсинга\n"
        "/subscriptions возвращает список активных подписок\n"
        "/unsubscribe [driver] [url] отписывает пользователя от обновлений\n"
        "параметры аналогичные /subscribe\n"
    )
    return msg.strip()


def _make_err(cmd: str):
    msg = (
        "Не удалось распарсить аргументы,\n"
        f"формат должен быть '/{cmd} [driver] [url]"
    )
    return msg


@dataclasses.dataclass(frozen=True)
class DriverUrl:
    driver: str
    url: str


def _parse_driver_url(
    args: typing.Optional[typing.List[str]],
) -> typing.Optional[DriverUrl]:
    if not args:
        return None
    if len(args) != 2:
        return None
    driver, url = args
    return DriverUrl(
        driver=driver,
        url=url,
    )


@tg_utils.simple_handler
def help(_: str) -> str:
    return _make_help()


@tg_utils.simple_handler
def start(chat_id: str) -> str:
    db = get_database()
    db.users.register(chat_id)
    return 'Вы успешно зарегистрированы!'


@tg_utils.simple_handler
def drivers(_: str):
    factory = driver_factory.DriverFactory()
    drivers_list = []
    for driver_type in sorted(factory.list()):
        drivers_list.append(f'`{driver_type}`')
    msg = '\n'.join(drivers_list)
    return msg


@tg_utils.simple_params_handler
def subscribe(chat_id: str, args: typing.List[str]):
    driver_url = _parse_driver_url(args)
    if not driver_url:
        return _make_err('subscribe')
    driver = driver_url.driver
    url = driver_url.url
    db = get_database()
    user_subscription = subscription.UserSubscription(db)
    if user_subscription.subscribe(chat_id, driver, url):
        return 'Вы успешно подписаны'
    return 'Не удалось создать фид'


@tg_utils.simple_params_handler
def unsubscribe(chat_id: str, args: typing.List[str]):
    driver_url = _parse_driver_url(args)
    if not driver_url:
        return _make_err('unsubscribe')
    driver = driver_url.driver
    url = driver_url.url
    db = get_database()
    user_subscription = subscription.UserSubscription(db)
    if user_subscription.unsubscribe(chat_id, driver, url):
        return 'Вы успешно отписаны'
    return 'Не удалось найти фид'


@tg_utils.simple_handler
def subscriptions(chat_id: str):
    db = get_database()
    user_subscription = subscription.UserSubscription(db)
    feeds = user_subscription.get_user_feeds(chat_id)
    data = []
    for feed in feeds:
        data.append(f'`{feed.get_driver()} {feed.get_url()}`')
    if not data:
        return 'Нет активных подписок'
    data_str = '\n'.join(sorted(data))
    msg = f'Активные подписки:\n{data_str}'
    return msg


def make_dispatcher(updater: telegram.ext.Updater) -> telegram.ext.Dispatcher:
    builder = tg_utils.DispatcherBuilder(updater)

    builder.add_handler('help', help)
    builder.add_handler('start', start)
    builder.add_handler('drivers', drivers)
    builder.add_params_handler('subscribe', subscribe)
    builder.add_params_handler('unsubscribe', unsubscribe)
    builder.add_handler('subscriptions', subscriptions)

    return builder.build()
