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

from modules import openvpn

from core import api
from core.helpers.log import hevlog
from core.helpers import elasticsearch

from multiprocessing import Process


hevlog = hevlog(level='debug')


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


# TODO: add threading support
# TODO: api needs to run in it's own thread
async def main(event_loop, CONF):
    hevlog.log('Main started')


def bootstrap():
    event_loop = asyncio.get_event_loop()

    try:
        event_loop.create_task(openvpn.build_client_configs.run(event_loop, CONF['config']['minio']))
        event_loop.create_task(elasticsearch.cleanup.run(event_loop, CONF['config']['elasticsearch']))
        event_loop.create_task(main(event_loop, CONF))
        event_loop.run_forever()
    except KeyboardInterrupt:
        hevlog.log('Interupted')
    finally:
        hevlog.log('Shutting down')
        hevlog.log('Closing loop')
        while event_loop.is_running():
            event_loop.close()
            if event_loop.is_closed():
                hevlog.log('Loop closed')
        hevlog.log('System off')


if __name__ == "__main__":
    jobs= []

    jobs.append(Process(target=api.statichev(CONF)))
    # jobs.append(Process(target=bootstrap()))

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
