import pytest
from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import mangaplus
import manga_notify.drivers.mangaplus.response_pb2 as pb


FEED_URL = 'https://mangaplus.shueisha.co.jp/titles/100191'
MOCK_URL = (
    'https://jumpg-webapi.tokyo-cdn.com/api/'
    'title_detailV2?title_id=100191'
)

MOCK_DATA = pb.Response(
    success_result=pb.SuccessResult(
        title_detail=pb.TitleDetailView(
            title=pb.Title(
                name='Oshi no Ko',
            ),
            chapters=pb.ChaptersView(
                last_chapter_list=[
                    pb.Chapter(
                        sub_title='Chapter 113: COMMERCIAL WORK',
                    )
                ],
            ),
        )
    )
)

TITLE = 'Oshi no Ko Chapter 113: COMMERCIAL WORK'
CURSOR = 'Chapter 113: COMMERCIAL WORK'

EXPECTED = (
   'Новый выпуск '
   f'[{TITLE}]'
   f'({FEED_URL})'
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
async def test_mangaplus(
    db_cursor,
    expected_message,
):
    driver = mangaplus.Mangaplus()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='mangaplus',
        url=FEED_URL,
        cursor=db_cursor,
    )

    with aioresponses() as mocked:
        mocked.get(
            MOCK_URL,
            status=200,
            body=MOCK_DATA.SerializeToString(),
        )
        parsing_result = await driver.parse(feed_data)

    assert parsing_result.feed_data.get_cursor() == CURSOR
    if not expected_message:
        assert not parsing_result.messages
    else:
        message = parsing_result.messages[0]
        assert message.serialize() == expected_message
