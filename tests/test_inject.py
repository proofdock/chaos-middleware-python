from unittest.mock import patch

from pdchaos import inject


@patch('pdchaos.inject.time')
def test_inject_delay(time):
    inject.delay(5)
    time.sleep.assert_called_once_with(5)
