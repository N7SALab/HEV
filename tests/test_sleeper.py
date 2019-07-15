from core.helpers import sleep


def test_seconds():
    sleep.seconds('test', 1)


def test_minutes():
    sleep.minutes('test', .001)

