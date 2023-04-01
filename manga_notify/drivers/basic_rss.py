import typing
import aiohttp

import xml.etree.ElementTree as ET

from . import driver
from . import common_message
from ..channels import channel
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
        yield common_message.ParsingItem(
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

    def _filter_item(self, item: common_message.ParsingItem) -> bool:
        """
        If true, item will be skipped during feed parsing
        """
        return False

    def _get_item(
        self,
        item: common_message.ParsingItem,
    ) -> common_message.ParsingItem:
        """
        Can be redefined in child class to
        sanitize title
        """
        return item

    async def parse(
        self,
        feed_data: feed_storage.FeedData,
    ) -> driver.ParsingResult:
        headers = {
            'User-Agent': UA,
        }

        async with aiohttp.ClientSession() as client:
            url = self._get_url(feed_data)
            async with client.get(
                url,
                headers=headers,
            ) as response:
                response.raise_for_status()
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
