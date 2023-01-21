import re

import pytest
from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import erai_raws_rss


URL = 'https://www.erai-raws.info/anime-list/nierautomata-ver1-1a/'
MOCK_URL = re.compile(
    r'^https:\/\/www\.erai-raws\.info\/anime-list'
    r'\/nierautomata-ver1-1a\/feed\/.*$'
)

XML = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"
xmlns:erai="https://www.erai-raws.info/rss-page/">

<channel>
  <title>NieR:Automata Ver1.1a - Erai-raws Torrent RSS</title>
  <item>
  <title>[Magnet] NieR:Automata Ver1.1a - 01 [SD][us][Airing]</title>
  <link>https://ddl2.erai-raws.info</link>
  <pubDate>Sat, 07 Jan 2023 17:42:51 +0000</pubDate>
  <description>
      DESCRIPTION
  </description>
  </item>
  <item>
  <title>[Torrent] NieR:Automata Ver1.1a - 01 [720p][us][Airing]</title>
  <link>magnet:123</link>
  <pubDate>Sat, 07 Jan 2023 17:42:51 +0000</pubDate>
  <description>
      DESCRIPTION
  </description>
  </item>
</channel>
</rss>
'''

CURSOR = (
    'Torrent NieR:Automata Ver1.1a - 01 '
    '720p us Airing'
)

TITLE = CURSOR

EXPECTED = (
   'Новый выпуск '
   f'[{TITLE}]'
   '(magnet:123)'
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'db_cursor,expected_message',
    (
        pytest.param(
            None,
            EXPECTED,
            id='first_run',
        ),
        pytest.param(
            CURSOR,
            None,
            id='no_new_episode',
        ),
    )
)
async def test_chapmanganato_bs(
    db_cursor,
    expected_message,
):
    driver = erai_raws_rss.EraiRawsRss()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='erai_raws_rss',
        url=URL,
        cursor=db_cursor,
    )

    with aioresponses() as mocked:
        mocked.get(
            MOCK_URL,
            status=200,
            body=XML,
        )
        parsing_result = await driver.parse(feed_data)

    assert parsing_result.feed_data.get_cursor() == CURSOR
    if not expected_message:
        assert not parsing_result.messages
    else:
        message = parsing_result.messages[0]
        assert message.serialize() == expected_message
