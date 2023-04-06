import pytest

from manga_notify.external import mal


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'response, expected',
    (
        pytest.param(
            {
                'id': 42,
                'title': 'Manga Title',
            },
            [
                mal.MyAnimeListItem(
                    title='Manga Title',
                    link='https://myanimelist.net/manga/42',
                ),
            ],
            id='found',
        ),
        pytest.param(
            None,
            [],
            id='not_found',
        ),
    )
)
async def test_mal(
    response,
    expected,
    mal_mock
):
    my_anime_list = mal.MyAnimeList()

    if response:
        mal_mock.add_manga(response['id'], response['title'])

    with mal_mock.mock():
        result = await my_anime_list.find('manga', 'test')
    assert result == expected
