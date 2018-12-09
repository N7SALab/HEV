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
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import (ThreadPoolExecutor, wait, as_completed)


from modules import openvpn

from core import api
from core.helpers.log import hevlog
from core.helpers import elasticsearch


hevlog = hevlog(level='info')


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


# TODO: add threading support
# TODO: api needs to run in it's own thread
def main():
    hevlog.log('Starting', main.__name__)
    hevlog.log('End', main.__name__)


def bootstrap():
    hevlog.log('Starting', bootstrap.__name__)

    pool = ThreadPoolExecutor(4)
    loop = asyncio.get_event_loop()

    futures = [
        pool.submit(main, loop, CONF),
        pool.submit(elasticsearch.cleanup.run, CONF['config']['elasticsearch']),
        pool.submit(openvpn.build_client_configs.run, CONF['config']['minio'])
    ]

    print(wait(futures))

    hevlog.log('End', bootstrap.__name__)


if __name__ == "__main__":
    processPool = ProcessPoolExecutor(2)

    futureProcesses = [
        processPool.submit(api.statichev, CONF),
        processPool.submit(bootstrap),
    ]
