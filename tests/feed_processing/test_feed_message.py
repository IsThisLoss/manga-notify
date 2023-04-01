import pytest

from manga_notify.feed_processing import feed_message
from manga_notify.drivers import driver


ONE = driver.ParsingItem(
    name='one.name',
    link='one.link',
)

TWO = driver.ParsingItem(
    name='two.name',
    link='two.link',
)

THREE = driver.ParsingItem(
    name='three.name',
    link='three.link',
)


@pytest.mark.parametrize(
    'items,expected_messages',
    (
        pytest.param(
            [],
            [],
            id='empty',
        ),
        pytest.param(
            [ONE],
            ['Новый выпуск [one.name](one.link)'],
            id='one_message',
        ),
        pytest.param(
            [ONE, TWO],
            [
                (
                    'Несколько новых выпусков:\n'
                    '[one.name](one.link)\n'
                    '[two.name](two.link)\n'
                ),
            ],
            id='multiple_messages',
        ),
        pytest.param(
            [ONE, TWO, THREE],
            [
                (
                    'Несколько новых выпусков:\n'
                    '[one.name](one.link)\n'
                    '[two.name](two.link)\n'
                ),
                'Новый выпуск [three.name](three.link)',
            ],
            id='split_by_chunks',
        ),
    )
)
def test_create_messages(
    items,
    expected_messages,
):
    messages = feed_message.create_messages(
        parsed_items=items,
        mal_url=None,
        chunk_size=2,
    )
    texts = list(message.serialize() for message in messages)
    assert texts == expected_messages
