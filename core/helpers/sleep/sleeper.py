import time
import random

from core.helpers.log import hevlog

hevlog = hevlog('sleeper', level='debug')


def day(caller):
    sleep = random.choice(range(1, 24 * 60 * 60))
    hevlog.log('sleeping for {} seconds'.format(sleep), caller, 'debug')
    return time.sleep(sleep)
