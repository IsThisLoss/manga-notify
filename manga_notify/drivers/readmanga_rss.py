from .basic_rss import BasicRss

from ..database import feed_storage


class ReadmangaRss(BasicRss):
    def is_match(self, url: str) -> bool:
        return 'readmanga' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Manga
