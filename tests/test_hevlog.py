from core.helpers.logger import Hevlog

hevlog = Hevlog('pytest', level='debug')


def test_hevlog():
    assert Hevlog
