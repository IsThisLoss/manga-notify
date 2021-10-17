import requests
import dataclasses

from bs4 import BeautifulSoup

from . import driver
from ..channels import channel
from ..database import feed_storage


class MangakakalotMessage(channel.Message):
    def __init__(self, name, link):
        self._name = name
        self._link = link

    def serialize(self) -> str:
        return f'Новый выпуск [{self._name}]({self._link})' 


@dataclasses.dataclass(frozen=True, order=True)
class ParsingItem:
    title: str
    link: str


class MangakakalotBs(driver.Driver):
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
            parsed_items.append(ParsingItem(
                title=title,
                link=href,
            ))

        if parsed_items:
            feed_data.set_cursor(parsed_items[0].title)
        messages = []
        for item in reversed(parsed_items):
            messages.append(MangakakalotMessage(
                item.title, item.link
            ))
        return driver.ParsingResult(
            feed_data=feed_data,
            messages=messages,
        )


if __name__ == '__main__':
    data = feed_storage.FeedData(feed_storage.FeedDataImpl(id='', driver='', url='https://mangakakalot.com/manga/dw925284', cursor=''))
    parser = MangakakalotBs()
    msgs = parser.parse(data).messages
    for msg in msgs:
        print(msg.serialize())
