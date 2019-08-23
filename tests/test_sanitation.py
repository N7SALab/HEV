from core.helpers import sanitation


def test_filename():
    test = 'handle-it.jpeg'
    result = test
    assert sanitation.string(test) == result


def test_simple_filename():
    test = 'handle.jpeg'
    result = test
    assert sanitation.string(test) == result


def test_bad_filename():
    test = 'handle:118//$1&1>2.jpeg'
    result = 'handle_118___1_1_2.jpeg'
    assert sanitation.string(test) == result


def test_dedup_list():
    test = [1, 1, 1, 1, 2, 3, 4]
    result = [1, 2, 3, 4]
    assert sanitation.dedup_list(test) == result
