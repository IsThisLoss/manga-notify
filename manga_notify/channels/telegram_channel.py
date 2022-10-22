import typing

import arq

from . import channel


class TelegramChannel(channel.Channel):
    """
    Channel of telegram user
    """

    def __init__(self, chat_id: str, redis: arq.connections.ArqRedis):
        self._chat_id = chat_id
        self._redis = redis

    async def send(self, message: channel.Message):
        await self._redis.enqueue_job(
            'send_telegram_message',
            self._chat_id,
            message.serialize(),
            message.extra(),
        )


class TelegramChannelFactory(channel.ChannelFactory):
    def __init__(self, redis: arq.connections.ArqRedis):
        self._redis = redis

    def get_channels(
        self,
        users: typing.List[str],
    ) -> typing.List[channel.Channel]:
        result: typing.List[channel.Channel] = []
        for user in users:
            result.append(TelegramChannel(user, self._redis))
        return result
