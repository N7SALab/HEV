#!/usr/bin/env python3
#
# api/v1
#

__version__ = '0.0.1'


import time
import json
import asyncio

from flask import (Flask, request, redirect, render_template)

from core.helpers.flask import config, auth
from core.helpers.log import *
from core.helpers.crypto import secret
from core.helpers.neo4j.cypher import neo4j_wrapper


try:
    CONF = json.load(open('/var/www/hev.conf'))
except:
    CONF = json.load(open('hev.conf'))


# Initializing app
app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.secret_key = secret.new_secret_key()
app.jinja_options = config.javascript_compatibility(app)


# User Management
login_manager = auth.login_manager_wrapper(app)
@login_manager.user_loader
def load_user(user_id):
    return auth.load_user(user_id)


# Neo4j
n = neo4j_wrapper(CONF)


@app.route('/', methods=['GET'])
def home(**args):
    """ Default home route

    """
    log('request: {}'.format(request))

    # process and send headers
    try:
        real_ip = auth.request_headers(request)['X-Real-IP']
        headers = dict(auth.request_headers(request))
        headers['Host'] = real_ip
    except:
        headers = dict(auth.request_headers(request))
    host = json.dumps(headers['Host'])
    for key in headers.keys():
        value = json.dumps(headers[key])
        data = {key: value}
        n.send_data('Headers', data)
        # create relationship from host to headers
        if key != 'Host':
            cypher = 'MATCH (host:Headers { `Host`: ' + host + ' }), (header:Headers { `' + key + '`: ' + value + '})\n'
            cypher += 'MERGE (host)-[:`Has header`]->(header)'
            n.create_relationship(cypher)

    start = time.time()

    authenticated, error = auth.login(request)

    return render_template('home.html', **locals()), print('Flask routing took:', time.time() - start)


@app.route('/authenticate', methods=['GET', 'POST'])
def login():
    """ User login page

    """
    log('request: {}'.format(request))

    title = 'Enter Universe'

    authenticated, error = auth.login(request)

    if authenticated:

        # TODO: Fix user redirect after login to either "?next=" or referrer
        return redirect('/')

    else:
        return render_template('login.html', **locals())


@app.route('/exit')
def logout():
    """ User is removed from flask_login session

    :return: executes flask_login.logout_user in browser session
    """
    log('request: {}'.format(request))

    auth.logout()

    return redirect('/')


async def hev():
    # this doesn't work as expected
    log('HEV is starting')

    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.create_task(hev())
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
