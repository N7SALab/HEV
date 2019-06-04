import re

from urllib.parse import urlencode
from datetime import datetime, timezone
from neo4j.v1 import GraphDatabase
from concurrent.futures import (ThreadPoolExecutor, wait)

from core.helpers.log import hevlog


hevlog = hevlog('neo4j', level='info')


def assert_label(label):
    """ Make sure neo4j label is formatted correctly
    """
    assert type(label) == str

    if type(label) != str:
        hevlog.logging.error('[assert_label] Label must be a string: {}'.format(label))

    if label:
        assert label
        if re.search('[:]', label):
            hevlog.logging.error(''''[assert_label] Invalid label '{}': Remove the colon from the label'''.format(label))
            return False

        if not re.search('[a-zA-Z]', label[0]):  # First letter of a label must be a letter
            hevlog.logging.error('''[assert_label] Invalid label '{}': First character of Neo4j :LABEL must be a letter'''.format(label))
            return False
        else:
            return ':`' + label + '`'  # :`Label`
    else:
        return ''


class Neo4jWrapper:
    """ Neo4j wrapper
    """

    def __init__(self, neo4j_config):
        self.user = neo4j_config['user']
        self.password = neo4j_config['password']
        self.servers = neo4j_config['servers']
        self.driver = self._try_servers(self.servers)

    def _try_servers(self, servers):

        pool = ThreadPoolExecutor(len(servers))

        futures = []

        for server in servers:
            futures.append(pool.submit(self._try_connect, server))

        finished, pending = wait(futures)

        for bolt in finished:
            if bolt.result():
                return bolt.result()

        return None

    def _try_connect(self, server):

        try:
            return GraphDatabase.driver(server, auth=(self.user, self.password))
        except:
            return False

    def _prepare_dict(self, blob):
        """ All inputs first needs to dicts
        """
        try:
            return dict(blob)
        except:
            return dict(raw=urlencode(blob))

    def _consolidate(self, query):
        """ Join cypher queries list into a string
        """
        return '\n'.join(query).strip()

    def _create_query(self, label, data):
        timestamp_date = datetime.now(tz=timezone.utc).isoformat()
        label = assert_label(label)

        if label is False:
            hevlog.logging.error('[_create_query] Query not created')
        else:
            node = 'header'
            dict_blob = self._prepare_dict(data)

            query = list()
            query.append('MERGE ( {} {} '.format(node, label))
            query.append('{')

            # iterate dict keys
            i = 0
            for key in dict_blob.keys():
                i = i + 1
                value = dict_blob[key]

                if i < len(dict_blob.keys()):
                    query.append('`{}`: {},'.format(key, value))
                else:
                    query.append('`{}`: {}'.format(key, value))

            query.append(' } )')

            query.append('ON CREATE SET {}.timestamp = "{}"'.format(node, timestamp_date))
            query.append('RETURN *')

            return query

    def _send(self, cypher):
        """ This is the query that will be run on the database. So make sure by the time it
            gets to this function all prior checks have passed. Also, create a last check in
            this function for general cypher query-ness
        """
        with self.driver.session() as session:
            results = session.run(cypher)

        hevlog.logging.debug('[send] Cypher: {}'.format(cypher))
        hevlog.logging.debug('[send] Results: {}'.format(results))

        return results

    def send_data(self, label, data):
        """ Just take the entry and put it into the database to be parsed later
        """
        query = self._create_query(label, data)
        final_cypher = self._consolidate(query)  # self._consolidate sets of queries into one single related query

        hevlog.logging.debug('[send data] {}'.format(final_cypher))

        return self._send(final_cypher)

    def create_node(self, cypher):
        """ Create node
        """
        hevlog.logging.debug('[create node] {}'.format(cypher))
        return self._send(cypher)

    def create_relationship(self, cypher):
        """ Create relationship
        """
        hevlog.logging.debug('[create relationship] {}'.format(cypher))
        return self._send(cypher)
