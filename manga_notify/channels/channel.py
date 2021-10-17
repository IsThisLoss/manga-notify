import abc


class Message:
    """
    Interface of diffenet type
    messages that could be sent to Channel
    """

    @abc.abstractmethod
    def serialize(self) -> str:
        pass


class Channel:
    """
    Interface of different type of
    channels
    """

    @abc.abstractmethod
    def send(self, msg: Message):
        pass
