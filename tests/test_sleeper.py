from core.helpers import sleeper


def test_seconds():
    sleeper.seconds('test', 1)


def test_minutes():
    sleeper.minutes('test', .001)

