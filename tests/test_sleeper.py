from core.helpers.sleeper import Sleeper


def test_seconds():
    Sleeper.seconds('test', 1)


def test_minutes():
    Sleeper.minutes('test', .001)

