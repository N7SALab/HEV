import time
import random

from core.helpers.log import hevlog

hevlog = hevlog('sleeper', level='debug')


def day(caller):
    sleep = random.choice(range(1, 24 * 60 * 60))
    hevlog.logging.debug('[{}] sleeping for {} seconds'.format(caller, sleep))
    return time.sleep(sleep)
