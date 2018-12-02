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
import threading

from modules import openvpn
from core.helpers.log import log
from core.helpers import elasticsearch


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


# TODO: add threading support
# TODO: api needs to run in it's own thread
async def main(event_loop, CONF):
    log('Main started')


if __name__ == "__main__":

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.create_task(openvpn.build_client_configs.run(event_loop, CONF['config']['minio']))
        event_loop.create_task(elasticsearch.cleanup.run(event_loop, CONF['config']['elasticsearch']))
        event_loop.create_task(main(event_loop, CONF))
        event_loop.run_forever()
    except KeyboardInterrupt:
        log('Interupted')
    finally:
        log('Shutting down')
        log('Closing loop')
        while event_loop.is_running():
            event_loop.close()
            if event_loop.is_closed():
                log('Loop closed')
        log('System off')
