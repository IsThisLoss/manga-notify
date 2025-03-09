import typing

from .basic_rss import BasicRss

from . import driver
from ..database import feed_storage
from .. import dependencies


class EraiRawsRss(BasicRss):
    def __init__(self):
        self._token = dependencies.get().get_cfg().erai_raws_token

    def is_match(self, url: str) -> bool:
        return bool(self._token) and 'erai-raws' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Anime

    def _get_url(self, feed_data: feed_storage.FeedData) -> str:
        url = feed_data.get_url()
        tail = f'feed/?token={self._token}'
        if url[-1] != '/':
            return url + '/' + tail
        return url + tail

    def _get_title(self, channel_title: str) -> str:
        parts = channel_title.split('-')
        idx = channel_title.rfind('-')
        if idx == -1:
            return channel_title
        return str(parts[0:idx]).strip()

    def _filter_item(self, item: driver.ParsingItem) -> bool:
        name = item.name.lower()
        is_match = 'torrent' in name and 'airing' in name
        is_match = is_match and ('us' in name or 'ru' in name)
        return not is_match

    def _get_item(
        self,
        item: driver.ParsingItem,
    ) -> driver.ParsingItem:
        return driver.ParsingItem(
            name=self.__fix_name(item.name),
            link=item.link,
        )

    def __fix_name(self, name: str) -> str:
        result: typing.List[str] = []
        for ch in name:
            if ch in ('[', ']'):
                ch = ' '
            if result and ch == ' ' and result[-1] == ' ':
                continue
            result.append(ch)
        return ''.join(result).strip()
