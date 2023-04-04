import typing

from ..external import mal


class MalSearchResponseBuilder:
    def __init__(self):
        self._msg = 'Ничего не нашлось'
        self._anime = []
        self._manga = []

    def add_anime(self, title: str, link: str):
        self._anime.append(f'[{title}]({link})')

    def add_manga(self, title: str, link: str):
        self._manga.append(f'[{title}]({link})')

    def serialize(self):
        if not self._anime and not self._manga:
            return 'Ничего не нашлось'
        result = 'Нашлось:\n'
        if self._manga:
            result += 'Манга:\n'
            result += '\n'.join(self._manga)
        if self._anime:
            result += 'Аниме:\n'
            result += '\n'.join(self._anime)
        return result


class MalSearch:
    def __init__(self):
        self._mal = mal.MyAnimeList()

    def search(
        self,
        text: str,
        limit: int = 1,
        feed_types: typing.Optional[typing.Optional[str]] = None,
    ):
        if not feed_types:
            feed_types = ['anime', 'manga']





