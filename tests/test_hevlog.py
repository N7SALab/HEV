from core.helpers.hevlog import Hevlog

hevlog = Hevlog('pytest', level='debug')


def test_hevlog():
    assert Hevlog
