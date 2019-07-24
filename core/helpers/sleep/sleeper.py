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


def minute(caller):
    """Sleep for a random minute
    """
    sleep = random.choice(range(1, 1 * 60))
    hevlog.logging.debug('[{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)


def minutes(caller, minutes):
    """Sleep for this many minutes
    """
    sleep = minutes * 60
    hevlog.logging.debug('[mins] [{}] sleeping for {} minutes'.format(caller, sleep))
    return time.sleep(sleep)


def hour(caller):
    """At some time within an hour, this will run
    """
    sleep = random.choice(range(1, 1 * 60 * 60))
    hevlog.logging.info('[hour] [{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)


def day(caller):
    """At some time within 24 hours, this will run
    """
    sleep = random.choice(range(1, 24 * 60 * 60))
    hevlog.logging.info('[day] [{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)


def time_range(caller, seconds):
    """Sleep for a random range
    """
    sleep = random.choice(range(1, seconds))
    hevlog.logging.debug('[range] [{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)
