import pytest
from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import mangaplus
from manga_notify.drivers.driver import ParsingItem
import manga_notify.drivers.mangaplus.response_pb2 as pb


FEED_URL = 'https://mangaplus.shueisha.co.jp/titles/100191'
MOCK_URL = (
    'https://jumpg-webapi.tokyo-cdn.com/api/title_detailV3'
    '?title_id=100191'
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
                        chapter_id=1015784,
                        sub_title='Chapter 113: COMMERCIAL WORK',
                    )
                ],
            ),
        )
    )
)

MOCK_DATA_ONLY_FIRST_CHAPTER_LIST = pb.Response(
    success_result=pb.SuccessResult(
        title_detail=pb.TitleDetailView(
            title=pb.Title(
                name='Oshi no Ko',
            ),
            chapters=pb.ChaptersView(
                first_chapter_list=[
                    pb.Chapter(
                        chapter_id=1015784,
                        sub_title='Chapter 113: COMMERCIAL WORK',
                    )
                ],
            ),
        )
    )
)

MOCK_DATA_BOTH_CHAPTER_LIST = pb.Response(
    success_result=pb.SuccessResult(
        title_detail=pb.TitleDetailView(
            title=pb.Title(
                name='Oshi no Ko',
            ),
            chapters=pb.ChaptersView(
                first_chapter_list=[
                    pb.Chapter(
                        chapter_id=1015783,
                        sub_title='Chapter 112',
                    )
                ],
                last_chapter_list=[
                    pb.Chapter(
                        chapter_id=1015784,
                        sub_title='Chapter 113: COMMERCIAL WORK',
                    )
                ],
            ),
        )
    )
)

TITLE = 'Oshi no Ko Chapter 113: COMMERCIAL WORK'
URL = 'https://mangaplus.shueisha.co.jp/viewer/1015784'
CURSOR = 'Chapter 113: COMMERCIAL WORK'
EXPECTED = ParsingItem(
    name=TITLE,
    link=URL,
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
            id='no_new_episode',
        ),
    )
)
async def test_mangaplus(
    db_cursor,
    expected_items,
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
    assert parsing_result.items == expected_items


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'mock_data',
    (
        pytest.param(
            MOCK_DATA_ONLY_FIRST_CHAPTER_LIST,
            id='only_first_chapter_list',
        ),
        pytest.param(
            MOCK_DATA_BOTH_CHAPTER_LIST,
            id='both_chapter_list',
        ),
    )
)
async def test_mangaplus_with_first_chapters(
    mock_data,
):
    driver = mangaplus.Mangaplus()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='mangaplus',
        url=FEED_URL,
        cursor='Chapter 112',
    )

    with aioresponses() as mocked:
        mocked.get(
            MOCK_URL,
            status=200,
            body=mock_data.SerializeToString(),
        )
        parsing_result = await driver.parse(feed_data)

    assert parsing_result.items == [EXPECTED]
