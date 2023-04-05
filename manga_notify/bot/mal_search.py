import asyncio
import logging
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

    def serialize(self) -> str:
        if not self._anime and not self._manga:
            return 'Ничего не нашлось'
        result = 'Нашлось:\n'
        if self._manga:
            result += 'Манга:\n'
            result += '\n'.join(self._manga)
        if self._anime:
            if self._manga:
                result += '\n'
            result += 'Аниме:\n'
            result += '\n'.join(self._anime)
        return result


class MalSearch:
    ANIME = 'anime'
    MANGA = 'manga'
    MIN_TEXT_LEN = 3
    QUICK_SEARCH_LIMIT = 1
    SEARCH_LIMIT = 5

    def __init__(self):
        self._mal = mal.MyAnimeList()

    async def quick_search(
        self,
        text: str,
    ) -> str:
        feed_types = set([self.MANGA, self.ANIME])
        if text.startswith(self.MANGA + ' '):
            text = text[len(self.MANGA)+1:]
            feed_types.remove(self.ANIME)
        elif text.startswith(self.ANIME + ' '):
            text = text[len(self.ANIME)+1:]
            feed_types.remove(self.MANGA)
        return await self._search(text, feed_types, self.QUICK_SEARCH_LIMIT)

    async def search(
        self,
        text: str,
    ) -> str:
        feed_types = set([self.MANGA, self.ANIME])
        return await self._search(text, feed_types, self.SEARCH_LIMIT)

    async def _search(
        self,
        text: str,
        feed_types: typing.Set[str],
        limit: int,
    ) -> str:
        result = MalSearchResponseBuilder()

        if len(text) < self.MIN_TEXT_LEN:
            return result.serialize()

        tasks = []
        if self.MANGA in feed_types:
            logging.info('Launch manga search task')
            tasks.append(asyncio.create_task(self._mal.find(self.MANGA, text, limit), name=self.MANGA))
        if self.ANIME in feed_types:
            logging.info('Launch anime search task')
            tasks.append(asyncio.create_task(self._mal.find(self.ANIME, text, limit), name=self.ANIME))

        done, _ = await asyncio.wait(tasks)
        for task in done:
            name = task.get_name()
            for item in task.result():
                if name == self.MANGA:
                    result.add_manga(item.title, item.link)
                elif name == self.ANIME:
                    result.add_anime(item.title, item.link)
                else:
                    logging.warning('Unknow task name %s', name)

        return result.serialize()
