import pytest

from aiogram import types

from manga_notify.bot import callback_data


def test_serializetion():
    data = callback_data.CallbackData(
        method='my_method',
        payload={
            'hello': 'world',
        },
    )
    serialized = data.serialize()
    assert serialized
    assert data == callback_data.parse(serialized)


@pytest.mark.parametrize(
    'matcher_method, is_matched',
    (
        pytest.param(
            'my_method',
            True,
            id='match',
        ),
        pytest.param(
            'another_method',
            False,
            id='do_not_match',
        ),
    )
)
def test_matcher(matcher_method, is_matched):
    data = callback_data.CallbackData(
        method='my_method',
        payload={},
    )
    serialized = data.serialize()
    query = types.CallbackQuery()
    query.data = serialized
    matcher = callback_data.create_matcher(matcher_method)
    assert matcher(query) == is_matched
