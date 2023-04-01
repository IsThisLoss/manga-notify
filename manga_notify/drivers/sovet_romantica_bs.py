import typing
import aiohttp

from bs4 import BeautifulSoup

from . import driver
from ..database import feed_storage


BASE_URL = 'https://sovetromantica.com'


class SovetRomanticaBs(driver.Driver):
    def is_match(self, url: str) -> bool:
        return 'sovetromantica' in url

    def feed_type(self) -> str:
        return feed_storage.FeedType.Anime

    def _get_anime_name(self, soup) -> typing.Optional[str]:
        anime_name = soup.find('div', class_='anime-name')
        if not anime_name:
            return None
        container = anime_name.find('div', class_='block--container')
        if not container:
            return None
        full_title = str(container.string)
        parts = full_title.split('/')
        if len(parts) != 2:
            return full_title
        return parts[1].strip()

    async def parse(
        self,
        feed_data: feed_storage.FeedData,
    ) -> driver.ParsingResult:
        async with aiohttp.ClientSession() as client:
            async with client.get(feed_data.get_url()) as response:
                response.raise_for_status()
                data = await response.text()

        soup = BeautifulSoup(data, 'html.parser')
        anime_name = self._get_anime_name(soup)
        if not anime_name:
            raise Exception("No anime name")
        feed_data.set_title(anime_name)
        episodes_slider = soup.find('div', {'id': 'episodes-slider'})
        if not episodes_slider:
            raise Exception("No episodes")
        episodes = episodes_slider.find_all('a')
        parsed_items = []
        db_cursor = -1
        if feed_data.get_cursor():
            db_cursor = int(feed_data.get_cursor())
        new_cursor = db_cursor
        for idx, episode in enumerate(episodes):
            if idx <= db_cursor:
                continue
            new_cursor = idx
            title = str(episode.find('span').string)
            href = episode.get('href')
            parsed_items.append(driver.ParsingItem(
                name=f'{anime_name} {title}',
                link=f'{BASE_URL}{href}',
            ))
        if parsed_items:
            feed_data.set_cursor(str(new_cursor))

        return driver.ParsingResult(
            feed_data=feed_data,
            items=parsed_items,
        )
