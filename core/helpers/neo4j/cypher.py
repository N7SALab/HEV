import re
import logging

from urllib.parse import urlencode
from datetime import datetime, timezone
from textwrap import dedent
from neo4j.v1 import GraphDatabase, basic_auth
from logging import DEBUG, INFO, ERROR, WARNING


# logging.basicConfig(level=WARNING)


def assert_label(label):
    """ Make sure neo4j label is formatted correctly
    """
    label = str(label)
    if label:
        if re.search('[:]', label):
            raise Exception('Invalid label \'{}\': Remove the colon from the label'.format(label))

        if not re.search('[a-zA-Z]', label[0]):  # First letter of a label must be a letter
            raise Exception(
                'Invalid label \'{}\': First character of Neo4j :LABEL must be a letter'.format(label))
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

        for server in self.servers:
            try:
                self.driver = GraphDatabase.driver(server, auth=(self.user, self.password))
                logging.info('Connected to neo4j server: {}'.format(server))
            except:
                logging.error('Cannot connect to neo4j server: {}'.format(server))

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

        logging.debug('Cypher: {}'.format(cypher))
        logging.debug('Results: {}'.format(results))

        return results

    def send_data(self, label, data):
        """ Just take the entry and put it into the database to be parsed later
        """
        query = self._create_query(label, data)
        final_cypher = self._consolidate(query)  # self._consolidate sets of queries into one single related query
    
        logging.debug(final_cypher)
    
        return self._send(final_cypher)

    def create_relationship(self, cypher):
        """ Create relationship
        """
        logging.debug(cypher)
        return self._send(cypher)
