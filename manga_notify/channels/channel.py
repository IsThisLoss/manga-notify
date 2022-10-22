import abc
import typing


class Message:
    """
    Interface of diffenet type
    messages that could be sent to Channel
    """

    @abc.abstractmethod
    def serialize(self) -> str:
        pass

    @abc.abstractmethod
    def extra(self) -> dict:
        return {}


class Channel:
    """
    Interface of different type of
    channels
    """

    @abc.abstractmethod
    async def send(self, msg: Message):
        pass


class ChannelFactory:
    @abc.abstractmethod
    def get_channels(self, users: typing.List[str]) -> typing.List[Channel]:
        pass
