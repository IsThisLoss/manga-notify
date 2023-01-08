import pytest

from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import animejoy_bs


URL = (
    'https://animejoy.ru/tv-serialy/'
    '2949-mobilnyy-voin-gandam-vedma-s-merkuriya.html'
)

HTML = '''
<html>
<head>
  <title>Test</title>
</head>
<body>
  <div class="titleup">
    <h1 class="h2 ntitle" itemprop="name">
      Мобильный воин Гандам: Ведьма с Меркурия [11 из 12]
    </h1>
    <h2 class="romanji">
      Mobile Suit Gundam: The Witch from Mercury
    </h2>
    <p class="editdate grey">Аниме обновлено:
      <b>25.12.2022 16:02 - Добавлена 11 серия с русскими субтитрами.</b>
    </p>
  </div>
</body>
</html>
'''

EXPECTED = (
   'Новый выпуск '
   '[Mobile Suit Gundam: The Witch from Mercury]'
   '(https://animejoy.ru/tv-serialy/2949-mobilnyy'
   '-voin-gandam-vedma-s-merkuriya.html)'
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
            '10',
            EXPECTED,
            id='new_episode',
        ),
        pytest.param(
            '11',
            None,
            id='no_new_episode',
        ),
    )
)
async def test_animejoy_bs(
    db_cursor,
    expected_message,
):
    driver = animejoy_bs.AnimeJoyBs()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='animejoy_bs',
        url=URL,
        cursor=db_cursor,
    )

    with aioresponses() as mocked:
        mocked.get(
            URL,
            status=200,
            body=HTML,
        )
        parsing_result = await driver.parse(feed_data)

    assert parsing_result.feed_data.get_cursor() == '11'
    if not expected_message:
        assert not parsing_result.messages
    else:
        message = parsing_result.messages[0]
        assert message.serialize() == expected_message
