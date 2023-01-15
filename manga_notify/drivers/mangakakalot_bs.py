import typing
import aiohttp

from bs4 import BeautifulSoup

from . import driver
from . import common_message
from ..channels import channel
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
            parsed_items.append(common_message.ParsingItem(
                name=title,
                link=href,
            ))

        messages: typing.List[channel.Message] = []
        if parsed_items:
            feed_data.set_cursor(parsed_items[0].name)
            items = list(reversed(parsed_items))
            messages = common_message.split_on_chunks(
                items,
                feed_data.get_mal_url(),
            )
        return driver.ParsingResult(
            feed_data=feed_data,
            messages=messages,
        )
