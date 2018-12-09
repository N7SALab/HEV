#!/usr/bin/env python3
#
# HEV Bootstrap Starter
#
#
#
# creator: ainiml
# created: Thu Oct 25 12:16:49 EDT 2018
#
#
# Usage: python3 run-hev.py
#

__version__ = '0.0.3'

import json
import asyncio

from multiprocessing import Process
from concurrent.futures import (ThreadPoolExecutor, wait,
                                as_completed)


from modules import openvpn

from core import api
from core.helpers.log import hevlog
from core.helpers import elasticsearch


hevlog = hevlog(level='debug')


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


# TODO: add threading support
# TODO: api needs to run in it's own thread
def main(event_loop=None, CONF=None):
    hevlog.log('Starting', main.__name__)


def bootstrap():
    hevlog.log('Starting', bootstrap.__name__, 'info')

    pool = ThreadPoolExecutor(4)
    loop = asyncio.get_event_loop()

    future = pool.submit(main, loop, CONF)

    print(future.result())


def async_bootstrap():
    event_loop = asyncio.get_event_loop()

    try:
        event_loop.create_task(openvpn.build_client_configs.run(event_loop, CONF['config']['minio']))
        event_loop.create_task(elasticsearch.cleanup.run(event_loop, CONF['config']['elasticsearch']))
        event_loop.create_task(main(event_loop, CONF))
        event_loop.run_until_complete(main(event_loop, CONF))
        # event_loop.run_forever()
    except KeyboardInterrupt:
        hevlog.log('Interupted', async_bootstrap.__name__)
    finally:
        hevlog.log('Shutting down', async_bootstrap.__name__)
        hevlog.log('Closing loop', async_bootstrap.__name__)
        while event_loop.is_running():
            event_loop.close()
            if event_loop.is_closed():
                hevlog.log('Loop closed', async_bootstrap.__name__)
        hevlog.log('System off', async_bootstrap.__name__)


if __name__ == "__main__":
    jobs= []

    jobs.append(Process(target=bootstrap()))
    # jobs.append(Process(target=async_bootstrap()))
    # jobs.append(Process(target=api.statichev(CONF)))

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
