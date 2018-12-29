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

import json

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import (ThreadPoolExecutor, wait, as_completed)

from core import api
from core.helpers.log import hevlog
from core.helpers import elasticsearch

from modules import openvpn


hevlog = hevlog('hev', level='debug')


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


def bootstrap():
    hevlog.logging.info('[bootstrap] Starting')

    pool = ThreadPoolExecutor(4)

    futures = [
        pool.submit(elasticsearch.cleanup.elasticsearch_cleaner, CONF['config']['elasticsearch']),
        pool.submit(openvpn.build_client_configs.run, CONF['config']['minio']),
    ]

    hevlog.logging.debug('[bootstrap] {}'.format(wait(futures)))
    hevlog.logging.debug('[bootstrap] all futures exited')


if __name__ == "__main__":
    processPool = ProcessPoolExecutor(4)

    futureProcesses = [
        processPool.submit(api.statichev, CONF),
        processPool.submit(bootstrap),
    ]

    hevlog.logging.debug('[main] {}'.format(wait(futureProcesses)))
    hevlog.logging.debug('[main] all processes exited')
