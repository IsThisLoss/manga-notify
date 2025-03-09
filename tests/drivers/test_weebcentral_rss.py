import pytest
from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import weebcentral
from manga_notify.drivers.driver import ParsingItem


URL = 'https://weebcentral.com/series/01J76XYA7MQA6QD2Y5C78X1BAS/rss'
MOCK_URL = 'https://weebcentral.com/series/01J76XYA7MQA6QD2Y5C78X1BAS/rss'

XML = '''<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
    <channel>
        <atom:link
            href="https://weebcentral.com/series/01J76XYA7MQA6QD2Y5C78X1BAS/rss"
            rel="self"
            type="application/rss+xml"
        />
        <title>Monthly Girls&#39; Nozaki-kun</title>
        <link>https://weebcentral.com/series/01J76XYA7MQA6QD2Y5C78X1BAS/Gekkan-Shojo-Nozaki-Kun</link>
        <lastBuildDate>Sun, 19 Jan 2025 03:08:25 +0000</lastBuildDate>
        <description>Monthly Girls&#39; Nozaki-kun Latest Updates</description>
        <language>en-us</language>
        <category>entertainment</category>
        <image>
            <url>https://temp.compsci88.com/cover/fallback/01J76XYA7MQA6QD2Y5C78X1BAS.jpg</url>
            <title>Monthly Girls&#39; Nozaki-kun</title>
            <link>https://weebcentral.com/series/01J76XYA7MQA6QD2Y5C78X1BAS/Gekkan-Shojo-Nozaki-Kun</link>
        </image>

        <item>
            <title>Monthly Girls' Nozaki-kun Issue 153</title>
            <link>https://weebcentral.com/chapters/01JHXFH58F3FZF83YAXG04VJQN</link>
            <pubDate>Sat, 18 Jan 2025 19:51:39 +0000</pubDate>
            <guid isPermaLink='false'>01JHXFH58F3FZF83YAXG04VJQN</guid>
        </item>

    </channel>
</rss>'''

CURSOR = "Monthly Girls' Nozaki-kun Issue 153"

TITLE = CURSOR

EXPECTED = ParsingItem(
   name=TITLE,
   link='https://weebcentral.com/chapters/01JHXFH58F3FZF83YAXG04VJQN',
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
            CURSOR,
            [],
            id='no_new_chapters',
        ),
    )
)
async def test_weebcentral_rss(
    db_cursor,
    expected_items,
):
    driver = weebcentral.WeebCentralRss()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='weebcentral_rss',
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
    assert parsing_result.items == expected_items
