from . import channel


class DummyChannel(channel.Channel):
    """
    Dummy channel, is used
    to validate feeds on its creation
    """

    def __init__(self):
        self.count = 0

    def send(self, _: channel.Message):
        self.count += 1
