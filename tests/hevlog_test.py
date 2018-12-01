# TODO: get pytest

from logging import INFO

from core.helpers.log import hevlog


def test_hevlog():
    result = hevlog()
    assert result is None or result is ''


if __name__ is '__main__':
    test_hevlog()
