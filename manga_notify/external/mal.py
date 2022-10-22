import typing
import aiohttp


class MyAnimeList:
    SEARCH_URL = 'https://api.myanimelist.net/v2/{feed_type}?q={title}&limit=1'
    WEB_URL = 'https://myanimelist.net/{feed_type}/{id}'
    CLIENT_ID = '6114d00ca681b7701d1e15fe11a4987e'

    async def find(self, feed_type: str, title: str) -> typing.Optional[str]:
        url = self.SEARCH_URL.format(feed_type=feed_type, title=title)
        headers = {
            'X-MAL-Client-ID': self.CLIENT_ID,
        }
        async with aiohttp.ClientSession() as client:
            async with client.get(url, headers=headers) as response:
                data = (await response.json())['data']
        if not data:
            return None
        title_id = data[0]['node']['id']
        return self.WEB_URL.format(feed_type=feed_type, id=title_id)
