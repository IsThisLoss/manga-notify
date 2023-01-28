from .basic_rss import BasicRss

from ..database import feed_storage


class ReadmangaRss(BasicRss):
    def is_match(self, url: str) -> bool:
        for name in ('readmanga', 'mintmanga'):
            if name in url:
                return True
        return False

    def feed_type(self) -> str:
        return feed_storage.FeedType.Manga
