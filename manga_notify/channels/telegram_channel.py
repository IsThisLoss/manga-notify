import telegram

from . import channel


class TelegramChannel(channel.Channel):
    """
    Channel of telegram user
    """

    def __init__(self, chat_id: str, bot: telegram.Bot):
        self._chat_id = chat_id
        self._bot = bot

    def send(self, message: channel.Message):
        self._bot.send_message(
            chat_id=self._chat_id,
            text=message.serialize(),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
