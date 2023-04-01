import aiohttp

from bs4 import BeautifulSoup

from . import driver
from ..database import feed_storage


class MangakakalotBs(driver.Driver):
    def is_match(self, url: str) -> bool:
        return 'mangakakalot' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Manga

    def chapter_list_class(self) -> str:
        return 'chapter-list'

    async def parse(
        self,
        feed_data: feed_storage.FeedData,
    ) -> driver.ParsingResult:

        async with aiohttp.ClientSession() as client:
            async with client.get(feed_data.get_url()) as response:
                response.raise_for_status()
                data = await response.text()

        soup = BeautifulSoup(data, 'html.parser')

        h1 = soup.find('h1')
        if h1:
            title = str(h1.string)
            feed_data.set_title(title)

        chapter_list = soup.find('div', class_=self.chapter_list_class())
        if not chapter_list:
            raise Exception("No chapters")
        chapters = chapter_list.find_all('a')
        parsed_items = []
        for charpter in chapters:
            title = str(charpter.string)
            href = str(charpter.get('href'))
            if title == feed_data.get_cursor():
                break
            parsed_items.append(driver.ParsingItem(
                name=title,
                link=href,
            ))

        if parsed_items:
            feed_data.set_cursor(parsed_items[0].name)
            parsed_items.reverse()

        return driver.ParsingResult(
            feed_data=feed_data,
            items=parsed_items,
        )
