from datetime import datetime

import pytest

from manga_notify.bot import remind_later



@pytest.mark.parametrize(
    'now, expected',
    (
        pytest.param(
            '2022-09-12',
            '2022-09-17',
            id='monday',
        ),
        pytest.param(
            '2022-09-13',
            '2022-09-17',
            id='tuesday',
        ),
        pytest.param(
            '2022-09-14',
            '2022-09-17',
            id='wednesday',
        ),
        pytest.param(
            '2022-09-15',
            '2022-09-17',
            id='thursday',
        ),
        pytest.param(
            '2022-09-16',
            '2022-09-17',
            id='friday',
        ),
        pytest.param(
            '2022-09-17',
            '2022-09-24',
            id='saturday',
        ),
        pytest.param(
            '2022-09-18',
            '2022-09-24',
            id='sunday',
        ),
    )
)
def test_find_next_saturday(now, expected):
    now_dt = datetime.strptime(now, '%Y-%m-%d')
    result = remind_later.find_next_saturday(now_dt)
    assert result.strftime('%Y-%m-%d') == expected
