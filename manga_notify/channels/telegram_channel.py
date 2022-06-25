import typing

import aiogram
from aiogram.types import ParseMode

from . import channel


class TelegramChannel(channel.Channel):
    """
    Channel of telegram user
    """

    def __init__(self, chat_id: str, bot: aiogram.Bot):
        self._chat_id = chat_id
        self._bot = bot

    async def send(self, message: channel.Message):
        await self._bot.send_message(
            self._chat_id,
            text=message.serialize(),
            parse_mode=ParseMode.MARKDOWN
        )


class TelegramChannelFactory(channel.ChannelFactory):
    def __init__(self, bot: aiogram.Bot):
        self._bot = bot

    def get_channels(
        self,
        users: typing.List[str],
    ) -> typing.List[channel.Channel]:
        result: typing.List[channel.Channel] = []
        for user in users:
            result.append(TelegramChannel(user, self._bot))
        return result
