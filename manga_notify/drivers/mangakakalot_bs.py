import typing
import requests

from bs4 import BeautifulSoup

from . import driver
from . import common_message
from ..channels import channel
from ..database import feed_storage


class MangakakalotBs(driver.Driver):
    def is_match(self, url: str) -> bool:
        return 'mangakakalot' in url

    def parse(self, feed_data: feed_storage.FeedData) -> driver.ParsingResult:

        response = requests.get(feed_data.get_url())

        soup = BeautifulSoup(response.text, 'html.parser')
        chapter_list = soup.find('div', class_='chapter-list')
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
            messages = common_message.split_on_chunks(items)
        return driver.ParsingResult(
            feed_data=feed_data,
            messages=messages,
        )
