import typing
import aiohttp

from . import response_pb2
from .. import driver
from ...database import feed_storage


UA = (
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) '
    'Gecko/20100101 Firefox/111.0'
)


class Mangaplus(driver.Driver):
    _API_URL = (
        'https://jumpg-webapi.tokyo-cdn.com/api/'
        'title_detailV2?title_id={manga_id}'
    )

    def is_match(self, url: str) -> bool:
        return 'mangaplus.shueisha.co.jp' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Manga

    def _get_url(self, feed_data: feed_storage.FeedData) -> str:
        # assuming url format is like
        # https://mangaplus.shueisha.co.jp/titles/100191
        manga_id = feed_data.get_url().split('/')[-1]
        return self._API_URL.format(manga_id=manga_id)

    def _format_item_name(
        self,
        title_name: typing.Optional[str],
        name: str,
    ) -> str:
        if not title_name:
            return name
        return f'{title_name} {name}'

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
                raw_data = await response.read()

        data = response_pb2.Response.FromString(raw_data)

        title_detail = data.success_result.title_detail
        if title_detail.title.name is not None:
            feed_data.set_title(str(title_detail.title.name))

        new_items = []
        for item in reversed(title_detail.chapters.last_chapter_list):
            if item.sub_title == feed_data.get_cursor():
                break
            new_items.append(driver.ParsingItem(
                name=item.sub_title,
                link=feed_data.get_url(),
            ))

        parsed_items = []
        if new_items:
            feed_data.set_cursor(new_items[0].name)
            for item in reversed(new_items):
                parsed_items.append(driver.ParsingItem(
                    name=self._format_item_name(
                        feed_data.get_title(),
                        item.name,
                    ),
                    link=item.link,
                ))

        return driver.ParsingResult(
            feed_data=feed_data,
            items=parsed_items,
        )
