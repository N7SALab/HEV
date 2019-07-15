from core.helpers.log import hevlog

hevlog = hevlog('pytest', level='debug')


def test_hevlog():
    assert hevlog
