import pytest

from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import chapmanganato_bs
from manga_notify.drivers.driver import ParsingItem


URL = 'https://chapmanganato.com/manga-th970764'

HTML = '''
<html>
<head>
  <title>Test</title>
</head>
<body>
  <h1>Poputepipikku</h1>
  <div class="panel-story-chapter-list">
    <ul class="row-content-chapter">
      <li class="a-h">
        <a rel="nofollow" class="chapter-name text-nowrap"
        href="https://chapmanganato.com/manga-th970764/chapter-63"
        title="Poputepipikku chapter Chapter 63">Chapter 63</a>
      </li>
    </ul>
  </div>
</body>
</html>
'''

EXPECTED = ParsingItem(
   name='Chapter 63',
   link='https://chapmanganato.com/manga-th970764/chapter-63',
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'db_cursor,expected_items',
    (
        pytest.param(
            None,
            [EXPECTED],
            id='first_run',
        ),
        pytest.param(
            'Chapter 63',
            [],
            id='no_new_episode',
        ),
    )
)
async def test_chapmanganato_bs(
    db_cursor,
    expected_items,
):
    driver = chapmanganato_bs.ChapmanganatoBs()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='chapmanganato_bs',
        url=URL,
        cursor=db_cursor,
    )

    with aioresponses() as mocked:
        mocked.get(
            URL,
            status=200,
            body=HTML,
        )
        parsing_result = await driver.parse(feed_data)

    assert parsing_result.feed_data.get_cursor() == 'Chapter 63'
    assert parsing_result.items == expected_items
