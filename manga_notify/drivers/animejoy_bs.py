import typing

from bs4 import BeautifulSoup

from . import driver
from .. import dependencies
from ..database import feed_storage


BASE_URL = 'https://animejoy.ru'


class AnimeJoyBs(driver.Driver):
    def is_match(self, url: str) -> bool:
        return 'animejoy' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Anime

    def _get_anime_name(self, soup) -> typing.Optional[str]:
        anime_name = soup.find('h2', class_='romanji')
        if not anime_name:
            return None
        return str(anime_name.string).strip()

    def _parse_cursor(self, soup) -> int:
        update_block = soup.find('p', class_='editdate grey')
        if not update_block:
            raise Exception("No update block")
        update_string = update_block.find('b')
        if not update_string:
            raise Exception("No update string")
        update_string = str(update_string.string).split(' ')[4]
        result = ''
        for ch in update_string:
            if not ch.isdigit():
                break
            result += ch
        return int(result)

    async def parse(
        self,
        feed_data: feed_storage.FeedData,
    ) -> driver.ParsingResult:
        client = await dependencies.get().get_http_client()
        async with client.get(feed_data.get_url()) as response:
            data = await response.text()

        soup = BeautifulSoup(data, 'html.parser')

        anime_name = self._get_anime_name(soup)
        if not anime_name:
            raise Exception("No anime name")
        feed_data.set_title(anime_name)

        db_cursor = -1
        if feed_data.get_cursor():
            db_cursor = int(feed_data.get_cursor())

        cur_cursor = self._parse_cursor(soup)

        parsed_items = []

        if cur_cursor > db_cursor:
            feed_data.set_cursor(str(cur_cursor))
            parsed_items.append(driver.ParsingItem(
                name=anime_name,
                link=feed_data.get_url(),
            ))

        return driver.ParsingResult(
            feed_data=feed_data,
            items=parsed_items,
        )
