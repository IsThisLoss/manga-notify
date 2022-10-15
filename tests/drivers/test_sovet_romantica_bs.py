import pytest

from aioresponses import aioresponses

from manga_notify.database import feed_storage
from manga_notify.drivers import sovet_romantica_bs

URL = 'http://sovetromantica.com/anime/spyxfamily'

HTML = '''
<html>
<head>
  <title>Test</title>
</head>
<body>
  <div class="episode-slick-container">
    <button class="episode-slick_button episode-slick_button-disabled" slider="episodes-slider" mode="backward">
      <i class="material-icons">keyboard_arrow_left</i>
    </button>
    <div class="episodes-slick" id="episodes-slider" style="scroll-behavior: smooth;">
      <div class="episodes-slick_item episode-active" id="num1">
       <a href="/anime/1382-spy-x-family-part-2/episode_1-subtitles" for="preview26228" class="">
          <img class="preview--poster lazy loaded" data-src="" src="" id="preview26228" alt="Эпизод 1" loading="lazy" data-was-processed="true">
          <div><span>Эпизод #1</span></div>
        </a>
        <nav class="episodeButtons"> </nav>
      </div>
      <div class="episodes-slick_item " id="num2">
        <a href="/anime/1382-spy-x-family-part-2/episode_2-subtitles" for="preview26266" class="">
          <img class="preview--poster lazy loaded" data-src="" src="" id="preview26266" alt="Эпизод 2" loading="lazy" data-was-processed="true">
          <div><span>Эпизод #2</span></div>
        </a>
      <nav class="episodeButtons"> </nav></div> </div>
      <button class="episode-slick_button" slider="episodes-slider" mode="forward">
      <i class="material-icons">keyboard_arrow_right</i>
    </button>
  </div>
  <div class="anime-info">
    <div class="block--container anime-info-block">
      <div class="block--full anime-name">
        <div class="block--container"> Семья шпиона. Часть 2 / Spy x Family Part 2 </div>
      </div>
    </div>
  </div>
</body>
</html>
'''

EXPECTED_TWO = (
  'Несколько новых выпусков:\n'
  '[ Семья шпиона. Часть 2 / Spy x Family Part 2  Эпизод #1]'
  '(https://sovetromantica.com/anime/1382-spy-x-family-part-2'
  '/episode_1-subtitles)\n'
  '[ Семья шпиона. Часть 2 / Spy x Family Part 2  Эпизод #2]'
  '(https://sovetromantica.com/anime/1382-spy-x-family-part-2'
  '/episode_2-subtitles)\n'
)

EXPECTED_ONE = (
   'Новый выпуск '
   '[ Семья шпиона. Часть 2 / Spy x Family Part 2  Эпизод #2]'
   '(https://sovetromantica.com/anime/1382-spy-x-family-part-2'
   '/episode_2-subtitles)'
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'db_cursor,expected_message',
    (
        pytest.param(
            None,
            EXPECTED_TWO,
            id='first_run',
        ),
        pytest.param(
            '0',
            EXPECTED_ONE,
            id='only_second_episode',
        ),
        pytest.param(
            '1',
            None,
            id='no_new_episode',
        ),
    )
)
async def test_sovet_romantica_bs(
    db_cursor,
    expected_message,
):
    driver = sovet_romantica_bs.SovetRomanticaBs()
    feed_data = feed_storage.FeedData(
        id=1,
        driver='sovet_romantica_bs',
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

    assert parsing_result.feed_data.get_cursor() == '1'
    if not expected_message:
        assert not parsing_result.messages
    else:
        message = parsing_result.messages[0]
        assert message.serialize() == expected_message
