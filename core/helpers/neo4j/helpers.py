import re
import asyncio

from urllib.parse import urlencode
from datetime import datetime, timezone
from neo4j.v1 import GraphDatabase, basic_auth

from core.helpers.log import hevlog


hevlog = hevlog(level='debug')


def assert_label(label):
    """ Make sure neo4j label is formatted correctly
    """
    assert type(label) == str

    if type(label) != str:
        hevlog.log('Label must be a string: {}'.format(label), assert_label.__name__, 'error')

    if label:
        assert label
        if re.search('[:]', label):
            hevlog.log(''''Invalid label '{}': Remove the colon from the label'''.format(label),
                       assert_label.__name__, 'error')
            return False

        if not re.search('[a-zA-Z]', label[0]):  # First letter of a label must be a letter
            hevlog.log('''Invalid label '{}': First character of Neo4j :LABEL must be a letter'''.format(label),
                       assert_label.__name__, 'error')
            return False
        else:
            return ':`' + label + '`'  # :`Label`
    else:
        return ''


class neo4j_wrapper:
    """ Neo4j wrapper
    """

    def __init__(self, conf):
        self.user = conf['config']['neo4j']['user']
        self.password = conf['config']['neo4j']['password']
        self.servers = conf['config']['neo4j']['servers']

        # TODO: make this async
        asyncloop = asyncio.get_event_loop()
        asyncloop.run_until_complete(self._try_servers(self.servers))

    async def _try_servers(self, servers):
        for server in servers:
            try:
                self.driver = await self._try_connect(server)
                hevlog.log('Connected to neo4j server: {}'.format(server), self._try_servers.__name__, 'info')
                break
            except:
                hevlog.log('Cannot connect to neo4j server: {}'.format(server), self._try_servers.__name__)

        return

    async def _try_connect(self, server):
        return GraphDatabase.driver(server, auth=(self.user, self.password))

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
            hevlog.log('Query not created', self._create_query.__name__, 'error')
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

        hevlog.log('Cypher: {}'.format(cypher), 'debug')
        hevlog.log('Results: {}'.format(results), 'debug')

        return results

    def send_data(self, label, data):
        """ Just take the entry and put it into the database to be parsed later
        """
        query = self._create_query(label, data)
        final_cypher = self._consolidate(query)  # self._consolidate sets of queries into one single related query

        hevlog.log(final_cypher, 'debug')

        return self._send(final_cypher)

    def create_node(self, cypher):
        """ Create node
        """
        hevlog.log(cypher, 'debug')
        return self._send(cypher)

    def create_relationship(self, cypher):
        """ Create relationship
        """
        hevlog.log(cypher, 'debug')
        return self._send(cypher)
