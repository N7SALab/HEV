#!/usr/bin/env python3
#
# HEV Bootstrap Starter
#
# Usage: python3 run-hev.py

import os

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import (ThreadPoolExecutor)

from core import api
from modules.openvpn import Openvpn
from modules.instagram import Instagram
from core.helpers.config import Config
from core.helpers.hevlog import Hevlog
from core.helpers.elasticsearch import ElasticsearchRun

hevlog = Hevlog('hev', level='debug')

CONF = Config()


def bootstrap():
    hevlog.logging.info('[bootstrap] Starting...')

    pool = ThreadPoolExecutor(4)

    futures = [
        pool.submit(ElasticsearchRun.clean_indexes, CONF.ELASTICSEARCH_HOSTS),
        pool.submit(Openvpn.build_client_configs,
                    CONF.MINIO_HOST, CONF.MINIO_ACCESS_KEY, CONF.MINIO_SECRET_KEY,
                    CONF.OPENVPN),
        pool.submit(Instagram.run_stories,
                    CONF.INSTAGRAM_USER, CONF.INSTAGRAM_PASSWORD, CONF.INSTAGRAM_FOLLOWING_LIST,
                    CONF.MINIO_HEV_HOST, CONF.MINIO_HEV_ACCESS_KEY, CONF.MINIO_HEV_SECRET_KEY),
    ]

    for future in futures:
        hevlog.logging.debug('[bootstrap] {} {}'.format(future, future.exception()))

    # hevlog.logging.debug('[bootstrap] {}'.format(wait(futures)))
    hevlog.logging.debug('[bootstrap] all futures exited')


if __name__ == "__main__":
    processPool = ProcessPoolExecutor(os.cpu_count())

    futureProcesses = [
        processPool.submit(api.statichev, CONF.NEO4J_USER, CONF.NEO4J_PASSWORD, CONF.NEO4J_SERVERS_LIST),
        processPool.submit(bootstrap),
    ]

    for future in futureProcesses:
        hevlog.logging.debug('[main] {} {}'.format(future, future.exception()))

    # hevlog.logging.debug('[main] {}'.format(wait(futureProcesses)))
    hevlog.logging.debug('[main] all processes exited')
