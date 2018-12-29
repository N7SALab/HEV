#!/usr/bin/env python3
#
# api/v1
#

__version__ = '0.0.1'


import time
import json

from flask import (Flask, request, redirect, render_template)

from core.helpers.log import hevlog
from core.helpers.crypto import secret
from core.helpers.neo4j.helpers import Neo4jWrapper

from core.helpers import flask as f


hevlog = hevlog('hevapi', level='debug')


# depreciated in 0.0.1
# removed 0.0.5
# try:
#     CONF = json.load(open('/var/www/hev.conf'))
# except:
#     CONF = json.load(open('hev.conf'))


# Initializing app
app = Flask(__name__, template_folder='../../web/templates', static_folder='../../web/static')
app.secret_key = secret.new_secret_key()
app.jinja_options = f.javascript_compatibility(app)


# User Management
login_manager = f.login_manager_wrapper(app)
@login_manager.user_loader
def load_user(user_id):
    return f.load_user(user_id)


@app.route('/', methods=['GET'])
def home(**args):
    """ Default home route
    """
    hevlog.logging.info('[home] request: {}'.format(request))

    # process and send headers
    try:
        real_ip = f.request_headers(request)['X-Real-IP']
        headers = dict(f.request_headers(request))
        headers['Host'] = real_ip
    except:
        headers = dict(f.request_headers(request))
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

    authenticated, error = f.login(request)

    return render_template('home.html', **locals()), print('Flask routing took:', time.time() - start)


@app.route('/authenticate', methods=['GET', 'POST'])
def login():
    """ User login page
    """
    hevlog.logging.info('[login] request: {}'.format(request))

    title = 'Hunt Everything'

    authenticated, error = f.login(request)

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
    hevlog.logging.info('[logout] request: {}'.format(request))

    logout()

    return redirect('/')


async def hev():
    # this doesn't work as expected
    hevlog.logging.info('[hev] HEV is starting')

    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', port=8080)


def statichev(CONF):
    # Neo4j
    global n
    n = Neo4jWrapper(CONF)

    hevlog.logging.info('[statichev] HEV is starting')

    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":

    try:
        CONF = json.load(open('/var/www/hev.conf'))
    except:
        CONF = json.load(open('hev.conf'))

    statichev(CONF)
