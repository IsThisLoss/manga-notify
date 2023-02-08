import typing
import aiohttp


class MyAnimeList:
    SEARCH_URL = 'https://api.myanimelist.net/v2/{feed_type}'
    WEB_URL = 'https://myanimelist.net/{feed_type}/{id}'
    CLIENT_ID = '6114d00ca681b7701d1e15fe11a4987e'

    async def find(self, feed_type: str, title: str) -> typing.Optional[str]:
        url = self.SEARCH_URL.format(feed_type=feed_type)
        headers = {
            'X-MAL-Client-ID': self.CLIENT_ID,
        }
        # for queries linger than 64 characters, mal returns bad_request
        params = {
            'q': title[:64],
            'limit': 1,
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
        if not data:
            return None
        title_id = data[0]['node']['id']
        return self.WEB_URL.format(feed_type=feed_type, id=title_id)
