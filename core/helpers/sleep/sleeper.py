import time
import random

from core.helpers.log import hevlog

hevlog = hevlog('sleeper', level='info')


def seconds(caller, seconds):
    """Sleep for this many seconds
    """
    sleep = seconds
    hevlog.logging.debug('[{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)


def hour(caller):
    """At some time within an hour, this will run
    """
    sleep = random.choice(range(1, 1 * 60 * 60))
    hevlog.logging.info('[{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)


def day(caller):
    """At some time within 24 hours, this will run
    """
    sleep = random.choice(range(1, 24 * 60 * 60))
    hevlog.logging.info('[{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)
