import abc
import dataclasses
import typing

from ..database import feed_storage


class DriverType(str):
    MangakakalotBs = 'mangakakalot_bs'
    MangaseeRss = 'mangasee_rss'
    ReadmangaRss = 'readmanga_rss'
    SovetRomanticaBs = 'sovet_romantica_bs'
    AnimeJoyBs = 'animejoy_bs'
    ChapmanganatoBs = 'chapmanganato_bs'
    EraiRawsRss = 'erai_raws_rss'
    Mangaplus = 'mangaplus'
    WeebCentralRss = 'weebcentral_rss'


@dataclasses.dataclass(frozen=True, order=True)
class ParsingItem:
    name: str
    link: str


@dataclasses.dataclass
class ParsingResult:
    """
    Describes result of Driver.parse method
    feed_data is updated feed data that should be
    put into storage
    items is list of new items extracted from
    data source since last run
    """
    feed_data: feed_storage.FeedData
    items: typing.List[ParsingItem]


class Driver:
    @abc.abstractmethod
    def is_match(self, url: str) -> bool:
        pass

    @abc.abstractmethod
    def feed_type(self) -> str:
        pass

    @abc.abstractmethod
    async def parse(self, feed_data: feed_storage.FeedData) -> ParsingResult:
        pass
