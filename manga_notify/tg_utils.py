import logging
import typing

import telegram
import telegram.ext


def simple_handler(fn: typing.Callable):
    """
    Decorator that pass char_id to function
    and sends return value of function as text
    """
    def wrapper(
        update: telegram.Update,
        context: telegram.ext.CallbackContext
    ):
        if not update.effective_chat:
            logging.warn('Got empty effective_chat')
            return
        chat_id = update.effective_chat.id
        msg = fn(chat_id)
        context.bot.send_message(
            chat_id=chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        return
    return wrapper


def simple_params_handler(fn: typing.Callable):
    """
    Decorator that pass char_id and args to function
    and sends return value of function as text
    """
    def wrapper(
        update: telegram.Update,
        context: telegram.ext.CallbackContext,
    ):
        if not update.effective_chat:
            logging.warn('Got empty effective_chat')
            return
        chat_id = update.effective_chat.id
        msg = fn(chat_id, context.args)
        context.bot.send_message(
            chat_id=chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        return
    return wrapper


class DispatcherBuilder:
    def __init__(self, updater: telegram.ext.Updater):
        self._dispatcher = updater.dispatcher

    def add_handler(self, command: str, handler: typing.Callable):
        self._dispatcher.add_handler(
            telegram.ext.CommandHandler(command, handler),
        )

    def add_params_handler(self, command: str, handler: typing.Callable):
        self._dispatcher.add_handler(
            telegram.ext.CommandHandler(command, handler, pass_args=True),
        )

    def build(self) -> telegram.ext.Dispatcher:
        return self._dispatcher
