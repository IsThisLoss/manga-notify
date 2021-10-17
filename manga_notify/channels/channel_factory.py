import typing

import telegram

from . import channel
from . import telegram_channel

from ..database import feed_storage
from ..database import user_storage


class ChannelFactory:
    def __init__(
        self,
        bot: telegram.Bot,
    ):
        self._bot = bot

    def get_channels(
        self,
        feed: feed_storage.FeedData,
        users: typing.List[user_storage.UserInfo],
    ) -> typing.List[channel.Channel]:
        result = []
        for user in users:
            if feed.get_id() in user.subscriptions:
                result.append(
                    telegram_channel.TelegramChannel(user.user_id, self._bot),
                )
        return result
