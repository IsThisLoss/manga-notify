import pytest

from manga_notify.bot import mal_search


@pytest.mark.asyncio
async def test_mal_search_empty(mal_mock):
    searcher = mal_search.MalSearch()

    with mal_mock.mock():
        result = await searcher.search('text')
        assert result == 'Ничего не нашлось'

    with mal_mock.mock():
        result = await searcher.quick_search('text')
        assert result == 'Ничего не нашлось'


@pytest.mark.asyncio
async def test_mal_search(mal_mock):
    searcher = mal_search.MalSearch()

    mal_mock.add_manga(1, 'manga_1')
    mal_mock.add_manga(2, 'manga_2')
    mal_mock.add_anime(3, 'anime_3')
    mal_mock.add_anime(4, 'anime_4')
    with mal_mock.mock():
        result = await searcher.search('text')

    assert result == (
        'Нашлось:\n'
        'Манга:\n'
        '[manga_1](https://myanimelist.net/manga/1)\n'
        '[manga_2](https://myanimelist.net/manga/2)\n'
        'Аниме:\n'
        '[anime_3](https://myanimelist.net/anime/3)\n'
        '[anime_4](https://myanimelist.net/anime/4)'
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'text,expected',
    (
        pytest.param(
            'text',
            (
                'Нашлось:\n'
                'Манга:\n'
                '[manga_1](https://myanimelist.net/manga/1)\n'
                'Аниме:\n'
                '[anime_1](https://myanimelist.net/anime/1)'
            ),
            id='both'
        ),
        pytest.param(
            'manga text',
            (
                'Нашлось:\n'
                'Манга:\n'
                '[manga_1](https://myanimelist.net/manga/1)'
            ),
            id='only_manga'
        ),
        pytest.param(
            'anime text',
            (
                'Нашлось:\n'
                'Аниме:\n'
                '[anime_1](https://myanimelist.net/anime/1)'
            ),
            id='only_anime'
        ),
    ),
)
async def test_mal_quick_search(text, expected, mal_mock):
    searcher = mal_search.MalSearch()

    mal_mock.add_manga(1, 'manga_1')
    mal_mock.add_anime(1, 'anime_1')
    with mal_mock.mock():
        result = await searcher.quick_search(text)

    assert result == expected


@pytest.mark.asyncio
async def test_mal_search_error(mal_mock):
    searcher = mal_search.MalSearch()

    mal_mock.set_status_code(500)
    with mal_mock.mock():
        result = await searcher.search('text')

    assert result == 'Похоже mal не работает'
