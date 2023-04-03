import dataclasses
import typing

import aiohttp


@dataclasses.dataclass
class MyAnimeListItem:
    title: str
    link: str


class MyAnimeList:
    SEARCH_URL = 'https://api.myanimelist.net/v2/{feed_type}'
    WEB_URL = 'https://myanimelist.net/{feed_type}/{id}'
    CLIENT_ID = '6114d00ca681b7701d1e15fe11a4987e'

    async def find(
        self,
        feed_type: str,
        title: str,
        limit: int = 1,
    ) -> typing.List[MyAnimeListItem]:
        url = self.SEARCH_URL.format(feed_type=feed_type)
        headers = {
            'X-MAL-Client-ID': self.CLIENT_ID,
        }
        # for queries linger than 64 characters, mal returns bad_request
        params = {
            'q': title[:64],
            'limit': limit,
        }
        async with aiohttp.ClientSession() as client:
            async with client.get(
                url,
                params=params,
                headers=headers,
            ) as response:
                response.raise_for_status()
                json = await response.json()
                data = json['data']

        result = []
        if not data:
            return result
        for item in data:
            node = item['node']
            title = node['title']
            link = self.WEB_URL.format(feed_type=feed_type, id=node['id'])
            result.append(MyAnimeListItem(
                title=title,
                link=link,
            ))
        return result
