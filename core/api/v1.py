#!/usr/bin/env python3
#
# api/v1
#

__version__ = '0.0.1'


import time
import json

from flask import (Flask, request, redirect, render_template)

from core.helpers.hevlog import Hevlog
from core.helpers import crypto
from core.helpers.neo4j import Neo4jWrapper

from core.helpers import flask as f

hevlog = Hevlog('hevapi', level='debug')


# Initializing app
app = Flask(__name__, template_folder='../../web/templates', static_folder='../../web/static')
app.secret_key = crypto.new_secret_key()
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
    start = int(time.time())

    # process and send headers
    headers = f.request_headers(request)

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

    authenticated, error = f.login(request)

    hevlog.logging.debug('[home] Flask routing took: {} seconds'.format(int(time.time()) - start))

    return render_template('home.html', **locals())


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


# authentication required
@app.route('/info')
def info():
    """ Show system information
    """
    return


# authentication required
@app.route('/dl/')


async def hev():
    # this doesn't work as expected
    hevlog.logging.info('[hev] HEV is starting')

    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', port=8080)


def statichev(neo4j_config):
    # Neo4j
    global n
    n = Neo4jWrapper(neo4j_config)

    hevlog.logging.info('[statichev] HEV is starting')

    # app.run(host='0.0.0.0', debug=True, port=8080)
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":

    try:
        CONF = json.load(open('../../hev.conf'))
    except:
        CONF = json.load(open('hev.conf'))

    statichev(CONF['neo4j'])
