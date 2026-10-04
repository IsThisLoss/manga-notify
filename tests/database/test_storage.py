from unittest.mock import AsyncMock

import pytest

from manga_notify.database import feed_storage, user_storage


@pytest.mark.asyncio
@pytest.mark.parametrize('method', ['get_all', 'find_without_mal_link'])
async def test_feed_selection(method):
    connection = AsyncMock()
    connection.fetch.return_value = [
        (1, 'manga', 'https://example.com/feed', 'cursor', 'Title', None),
    ]
    storage = feed_storage.FeedStorage(connection)

    feeds = await getattr(storage, method)()

    assert len(feeds) == 1
    assert feeds[0].get_id() == 1
    assert feeds[0].get_title() == 'Title'
    assert feeds[0].get_cursor() == 'cursor'
    if method == 'find_without_mal_link':
        assert connection.fetch.await_args.args[1:] == (10,)


@pytest.mark.asyncio
async def test_user_subscriptions():
    connection = AsyncMock()
    connection.fetch.return_value = [(1,), (2,)]
    storage = user_storage.UserStorage(connection)

    result = await storage.get_subscriptions('42')

    assert result == user_storage.UserInfo('42', {1, 2})
    assert connection.fetch.await_args.args[1:] == ('42',)


@pytest.mark.asyncio
async def test_all_user_subscriptions():
    connection = AsyncMock()
    connection.fetch.return_value = [('42', 1), ('42', 2), ('43', 2)]
    storage = user_storage.UserStorage(connection)

    result = await storage.get_all()

    assert result == [
        user_storage.UserInfo('42', {1, 2}),
        user_storage.UserInfo('43', {2}),
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize('exists', [True, False])
async def test_user_exists(exists):
    connection = AsyncMock()
    connection.fetchval.return_value = exists
    storage = user_storage.UserStorage(connection)

    assert await storage.exists('42') is exists
    assert connection.fetchval.await_args.args[1:] == ('42',)
