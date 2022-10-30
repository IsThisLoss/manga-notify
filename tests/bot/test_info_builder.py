from manga_notify.database import feed_storage
from manga_notify.bot import info_builder


def test_info_builder():
    feed = feed_storage.FeedData(
        id=1,
        driver='driver',
        url='http://feed_url',
        cursor='',
        title='My Title',
        mal_url='http://mal_url'
    )

    result = info_builder.build_feed_info(feed)
    assert result == (
        'My Title:\n'
        '- `http://feed_url`\n'
        '- [MAL](http://mal_url)\n'
    )
