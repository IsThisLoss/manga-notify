import contextlib
import json
import re

from aioresponses import aioresponses
import pytest


@pytest.fixture()
def mal_mock():
    class Context:
        MANGA_URL = re.compile(r'^https://api\.myanimelist\.net/v2/manga.*$')
        ANIME_URL = re.compile(r'^https://api\.myanimelist\.net/v2/anime.*$')

        def __init__(self):
            self.anime = []
            self.manga = []

        def _make_node(self, id: int, title: str) -> dict:
            return {
                'node': {
                    'id': id,
                    'title': title,
                },
            }

        def add_manga(self, id: int, title: str):
            self.manga.append(self._make_node(id, title))

        def add_anime(self, id: int, title: str):
            self.anime.append(self._make_node(id, title))

        @contextlib.contextmanager
        def mock(self):
            with aioresponses() as mocked:
                mocked.get(
                    self.MANGA_URL,
                    status=200,
                    body=json.dumps({
                        'data': ctx.manga,
                    }),
                )
                mocked.get(
                    self.ANIME_URL,
                    status=200,
                    body=json.dumps({
                        'data': ctx.anime,
                    }),
                )
                yield

    ctx = Context()
    return ctx
