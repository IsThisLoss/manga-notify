from .basic_rss import BasicRss

from ..database import feed_storage
from .. import dependencies
from . import common_message


class EraiRawsRss(BasicRss):
    def __init__(self):
        self._token = dependencies.get().get_cfg().erai_raws_token

    def is_match(self, url: str) -> bool:
        return bool(self._token) and 'erai-raws' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Anime

    def filter_item(self, item: common_message.ParsingItem) -> bool:
        is_match = (
            'Torrent' in item.name
            and
            '720p' in item.name
        )
        return not is_match

    def decorate_url(self, url: str) -> str:
        tail = f'feed/?{self._token}'
        if url[-1] != '/':
            return url + '/' + tail
        return url + tail
