import re

import pytest

from aioresponses import aioresponses

SEARCH_URL = re.compile(r'^https://api\.myanimelist\.net/v2/.*$')


def make_mal_response_entry(id: int, title: str) -> dict:
    return {
        'node': {
            'id': id,
            'title': title,
        },
    }


@pytest.mark.asyncio
async def test_mal_search(
):
