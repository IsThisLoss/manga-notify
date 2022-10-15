import abc
import dataclasses
import typing

from ..channels import channel
from ..database import feed_storage


class DriverType(str):
    MangaseeRss = 'mangasee_rss'
    MangakakalotBs = 'mangakakalot_bs'
    ReadmangaRss = 'readmanga_rss'


@dataclasses.dataclass
class ParsingResult:
    """
    Describes result of Driver.parse method
    feed_data is updated feed data that should be
    put into storage
    messages is list of new messages extracted from
    data source since last run
    """
    feed_data: feed_storage.FeedData
    messages: typing.List[channel.Message]


class Driver:
    @abc.abstractmethod
    def is_match(self, url: str) -> bool:
        pass

    @abc.abstractmethod
    async def parse(self, feed_data: feed_storage.FeedData) -> ParsingResult:
        pass
