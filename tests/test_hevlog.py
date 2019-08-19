from core.helpers.logger import hevlog

hevlog = hevlog('pytest', level='debug')


def test_hevlog():
    assert hevlog
