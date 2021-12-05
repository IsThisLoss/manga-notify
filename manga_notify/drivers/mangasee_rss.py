import typing
import requests
import dataclasses

import xml.etree.ElementTree as ET

from . import driver
from ..channels import channel
from ..database import feed_storage


UA = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) '
    'Gecko/20100101 Firefox/93.0'
)


class MangaseeMessage(channel.Message):
    def __init__(self, name, link):
        self._name = name
        self._link = link

    def serialize(self) -> str:
        return f'Новый выпуск [{self._name}]({self._link})'


@dataclasses.dataclass
class ParsingItem:
    title: str
    link: str


def iter_items(items):
    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        if not title:
            continue
        yield ParsingItem(
            title=title,
            link=link,
        )


class MangaseeRss(driver.Driver):
    def parse(self, feed_data: feed_storage.FeedData) -> driver.ParsingResult:
        headers = {
            'User-Agent': UA,
        }

        response = requests.get(feed_data.get_url(), headers=headers)
        root = ET.fromstring(response.text)
        parsed_items = []
        for item in iter_items(root.findall('./channel/item')):
            if item.title == feed_data.get_cursor():
                break
            parsed_items.append(item)
        if parsed_items:
            feed_data.set_cursor(parsed_items[0].title)
        messages: typing.List[channel.Message] = []
        for item in reversed(parsed_items):
            messages.append(MangaseeMessage(
                item.title, item.link
            ))
        return driver.ParsingResult(
            feed_data=feed_data,
            messages=messages,
        )
