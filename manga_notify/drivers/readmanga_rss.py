from .basic_rss import BasicRss


class ReadmangaRss(BasicRss):
    def is_match(self, url: str) -> bool:
        return 'readmanga' in url
