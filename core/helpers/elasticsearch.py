import warnings
import datetime
import elasticsearch

from elasticsearch import Elasticsearch, RequestsHttpConnection


from core.helpers.sleeper import Sleeper
from core.helpers.hevlog import Hevlog

hevlog = Hevlog('elasticsearch', level='info')


# TODO: These are expecting an Elasticsearch object
async def es_wrapper(hosts):
    """ A wrapper for Elastcisearch

    """
    warnings.warn('This library is no longer used', DeprecationWarning)
    hevlog.logging.debug('[es_wrapper] Connecting to Elasticsearch')

    return await Elasticsearch(hosts)


async def send_doc(es):
    """ Send a document to Elasticsearch

    """
    warnings.warn('This library is no longer used', DeprecationWarning)

    hevlog.logging.debug('[send_doc] Sending doc')
    return


async def get_alias(es, alias='*'):
    """ Query Elasticsearch for alias

    """
    warnings.warn('This library is no longer used', DeprecationWarning)

    hevlog.logging.debug('[get_alias] Get alias: {}'.format(alias))
    return await es.indices.get_alias(alias)


async def get_indice(es, index='*'):
    """ Query Elasticsearch for index

    """
    warnings.warn('This library is no longer used', DeprecationWarning)

    hevlog.logging.debug('[get_indice] Get index: {}'.format(index))
    return await es.indices.get(index)


async def info(es):
    """ Get info on Elasticsearch cluster

    """
    warnings.warn('This library is no longer used', DeprecationWarning)

    hevlog.logging.debug('[info] Cluster info')
    return await es.info()


async def ping(es):
    """ Ping Elasticsearch cluster

    """
    warnings.warn('This library is no longer used', DeprecationWarning)

    hevlog.logging.debug('[ping] Ping Elasticsearch cluster')
    return await es.ping()


class ElasticsearchConnect:

    def __init__(self, host=['elasticsearch'], request_timeout=10,
                 http_auth=None, use_ssl=True, verify_certs=True,
                 connection_class=RequestsHttpConnection):
        """

        :param host:
        :param request_timeout:
        :param http_auth:
        :param use_ssl:
        :param verify_certs:
        :param connection_class:
        """

        for _host in host:
            try:
                self.wrapper = Elasticsearch(
                    hosts=[_host],
                    request_timeout=request_timeout,
                    http_auth=http_auth,
                    use_ssl=use_ssl,
                    verify_certs=verify_certs,
                    connection_class=connection_class
                )
                break
            except:
                self.wrapper = None
            finally:
                if self.wrapper is None:
                    hevlog.logging.error('No elasticsearch hosts available')
                    raise Exception('No elasticsearch hosts available')

        self.host = host
        self.cache = []
        self.indices = []

    def search_indices(self, index_pattern):
        try:
            retrieved_indices = self.wrapper.indices.get(index_pattern)
            num_indices = len(retrieved_indices)

            msg = 'Search found {} indices'.format(num_indices)
            hevlog.logging.info('[search indices] {}'.format(msg))
            return retrieved_indices
        except elasticsearch.exceptions.NotFoundError:
            msg = '''You provided the index pattern '{}', but searches returned fruitless'''
            msg = msg.format(index_pattern)
            hevlog.logging.error('[search indices] {}'.format(msg))

    def delete_indices(self, index_pattern):

        retrieved_indices = [x for x in self.search_indices(index_pattern).keys()]
        num_indices = len(retrieved_indices)

        msg = 'Search found {} indices'.format(num_indices)
        hevlog.logging.info('[delete indices] {}'.format(msg))

        if not num_indices:
            msg = '''No indices found. exiting'''
            print(msg)
            return False

        for index in retrieved_indices:
            print(index)

        # TODO: Find a way to undo index deletions
        #       One way could be to rename the indices and store a link to the new
        #       indices in a node of deleted indices
        if num_indices < 2:
            msg = '''\nYOU'RE ABOUT TO DELETE {} INDEX! ARE YOU SURE YOU WANT TO CONTINUE? '''
        elif num_indices > 1:
            msg = '''\nYOU'RE ABOUT TO DELETE {} INDICES! ARE YOU SURE YOU WANT TO CONTINUE? '''
        msg += '''THIS CANNOT BE UNDONE! DECIDE WISELY [y/N]'''
        msg = msg.format(num_indices)
        print(msg)

        answer = str(input()).lower()

        if not answer:
            answer = 'N'

        if answer == 'y':
            for index in retrieved_indices:
                msg = '''Deleting {}...'''
                msg = msg.format(index)
                print(msg, end='')
                # Delete the index
                self.wrapper.indices.delete(index=index)
                print('done')
        else:
            msg = '''Whew, you might have just blew it, if you had said yes'''
            print(msg)

    def get_indices(self):
        retrieved_indices = self.wrapper.indices.get('*')
        num_indices = len(retrieved_indices)

        self.indices = retrieved_indices
        msg = 'Retrieved {} indices'.format(num_indices)
        hevlog.logging.debug('[get indices] {}'.format(msg))


def clean_indexes(elasticsearch_config):
    hevlog.logging.info('Running...')

    # TODO: this might create too many connections to elasticsearch
    while True:

        es = ElasticsearchConnect(elasticsearch_config['hosts'], use_ssl=False, request_timeout=40)

        hevlog.logging.debug('[elasticsearch cleaner] {}'.format(es.wrapper.info()))
        hevlog.logging.debug('[elasticsearch cleaner] {}'.format(es.get_indices()))

        DAYS = 14

        pattern = '*'
        search = es.search_indices(pattern)
        keys = sorted(list(search.keys()))

        # ignore these indices
        ignore = [
            '.kibana',
            '.kibana_1',
            '.kibana_2',
            '.kibana_3'
        ]

        for _key in ignore:
            if _key in keys:
                keys.remove(_key)

        for alias in keys:
            # indices = get_indice(es, alias)
            indices = es.wrapper.indices.get(alias)

            creation_date = indices[alias]['settings']['index']['creation_date']
            creation_date = int(creation_date)

            # month old
            month = datetime.timedelta(days=DAYS)
            today = datetime.datetime.today()
            past = today - month
            epoch = past - datetime.datetime.utcfromtimestamp(0)
            delete_older = int(epoch.total_seconds()) * 1000

            if creation_date < delete_older:
                # delete index
                # es.indices.delete(alias, ignore=[400, 404])
                es.wrapper.indices.delete(alias)
                hevlog.logging.info('[elasticsearch cleaner] deleted {}'.format(alias))

        hevlog.logging.info('[ElasticsearchConnect] done')
        hevlog.logging.debug('[ElasticsearchConnect] sleeping')
        Sleeper.day('elasticsearch cleanup')
