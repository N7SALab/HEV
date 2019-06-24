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

__version__ = '0.0.4'

import os
import json

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import (ThreadPoolExecutor)

from core import api
from core.helpers.log import hevlog

from modules import instagram

hevlog = hevlog('hev', level='debug')


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


def bootstrap():
    hevlog.logging.info('[bootstrap] Starting')

    pool = ThreadPoolExecutor(4)

    futures = [
        pool.submit(core.helpers.elasticsearch.index_cleanup.run, CONF['elasticsearch']),
        pool.submit(modules.openvpn.build_client_configs.run, CONF['minio']),
        pool.submit(instagram.run, CONF['instagram']),
    ]

    for future in futures:
        hevlog.logging.debug('[bootstrap] {} {}'.format(future, future.exception()))

    # hevlog.logging.debug('[bootstrap] {}'.format(wait(futures)))
    hevlog.logging.debug('[bootstrap] all futures exited')


if __name__ == "__main__":
    processPool = ProcessPoolExecutor(os.cpu_count())

    futureProcesses = [
        processPool.submit(api.statichev, CONF['neo4j']),
        processPool.submit(bootstrap),
    ]

    for future in futureProcesses:
        hevlog.logging.debug('[main] {} {}'.format(future, future.exception()))

    # hevlog.logging.debug('[main] {}'.format(wait(futureProcesses)))
    hevlog.logging.debug('[main] all processes exited')

