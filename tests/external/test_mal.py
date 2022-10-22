import json
import re

import pytest

from aioresponses import aioresponses

from manga_notify.external import mal


SEARCH_URL = re.compile(r'^https://api\.myanimelist\.net/v2/.*$')


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'response, expected_url',
    (
        pytest.param(
            {
                'data': [
                    {
                        'node': {
                            'id': 42,
                        },
                    },
                ],
            },
            'https://myanimelist.net/manga/42',
            id='found',
        ),
        pytest.param(
            {
                'data': [],
            },
            None,
            id='not_found',
        ),
    )
)
async def test_mal(
    response,
    expected_url,
):
    my_anime_list = mal.MyAnimeList()
    with aioresponses() as mocked:
        mocked.get(
            SEARCH_URL,
            status=200,
            body=json.dumps(response),
        )
        result = await my_anime_list.find('manga', 'test')
    assert result == expected_url
