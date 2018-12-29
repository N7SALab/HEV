from elasticsearch import Elasticsearch

from core.helpers.log import hevlog

hevlog = hevlog('elasticsearch', level='info')


# TODO: These are expecting an Elasticsearch object


async def es_wrapper(hosts):
    """ A wrapper for Elastcisearch

    """
    hevlog.logging.debug('[es_wrapper] Connecting to Elasticsearch')

    return await Elasticsearch(hosts)


async def send_doc(es):
    """ Send a document to Elasticsearch

    """
    hevlog.logging.debug('[send_doc] Sending doc')
    return


async def get_alias(es, alias='*'):
    """ Query Elasticsearch for alias

    """
    hevlog.logging.debug('[get_alias] Get alias: {}'.format(alias))
    return await es.indices.get_alias(alias)


async def get_indice(es, index='*'):
    """ Query Elasticsearch for index

    """
    hevlog.logging.debug('[get_indice] Get index: {}'.format(index))
    return await es.indices.get(index)


async def info(es):
    """ Get info on Elasticsearch cluster

    """
    hevlog.logging.debug('[info] Cluster info')
    return await es.info()


async def ping(es):
    """ Ping Elasticsearch cluster

    """
    hevlog.logging.debug('[ping] Ping Elasticsearch cluster')
    return await es.ping()
