from urllib.parse import urlparse

import xml.etree.ElementTree as ET

from . import driver
from .. import dependencies
from ..database import feed_storage


UA = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) '
    'Gecko/20100101 Firefox/93.0'
)


def iter_items(items):
    for item in items:
        title = item.find('title').text
        link = item.find('link').text
        if not title:
            continue
        yield driver.ParsingItem(
            name=title,
            link=link,
        )


class BasicRss(driver.Driver):
    def is_match(self, url: str) -> bool:
        raise NotImplementedError

    def _get_url(self, feed_data: feed_storage.FeedData) -> str:
        """
        Can be redefined in child class to pass secret
        parameters to url
        """
        return feed_data.get_url()

    def _get_title(self, channel_title: str) -> str:
        """
        Can be redefined in child class
        to modify title
        """
        return channel_title

    def _filter_item(self, item: driver.ParsingItem) -> bool:
        """
        If true, item will be skipped during feed parsing
        """
        return False

    def _get_item(
        self,
        item: driver.ParsingItem,
    ) -> driver.ParsingItem:
        """
        Can be redefined in child class to
        sanitize title
        """
        return item

    async def parse(
        self,
        feed_data: feed_storage.FeedData,
    ) -> driver.ParsingResult:
        url = self._get_url(feed_data)
        host = urlparse(url).netloc

        headers = {
            'User-Agent': UA,
            'Accept': '*/*',
            'Host': host,
        }

        client = await dependencies.get().get_http_client()
        async with client.get(
            url,
            headers=headers,
        ) as response:
            data = await response.text()

        root = ET.fromstring(data)

        title = root.find('./channel/title')
        if title is not None:
            feed_data.set_title(str(title.text))

        parsed_items = []
        for item in iter_items(root.findall('./channel/item')):
            item = self._get_item(item)
            if self._filter_item(item):
                continue
            if item.name == feed_data.get_cursor():
                break
            parsed_items.append(item)

        if parsed_items:
            feed_data.set_cursor(parsed_items[0].name)
            parsed_items.reverse()

        return driver.ParsingResult(
            feed_data=feed_data,
            items=parsed_items,
        )
