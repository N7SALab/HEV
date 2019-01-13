import datetime
import elasticsearch

from elasticsearch import Elasticsearch, RequestsHttpConnection

from core.helpers.log import hevlog
from core.helpers.sleep import sleeper


hevlog = hevlog('elasticsearch', level='info')


class ElasticsearchConnect:

    # TODO: move port into configuration file
    def __init__(self, host=['elasticsearch'], port=9200, request_timeout=10,
                 http_auth=None, use_ssl=True, verify_certs=True,
                 connection_class=RequestsHttpConnection):

        if host == list():
            hevlog.logging.error('No elasticsearch hosts given')
            raise Exception('No elasticsearch hosts given')

        for _host in host:
            try:
                self.wrapper = Elasticsearch(
                    hosts=[{'host': _host, 'port': port}],
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
        self.port = port
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
        hevlog.logging.info('[delete indices] {}'.foramt(msg))

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


def run(elasticsearch_config):

    # TODO: this might create too many connections to elasticsearch
    while True:

        es = ElasticsearchConnect(elasticsearch_config['hosts'], use_ssl=False, request_timeout=40)

        hevlog.logging.debug('[elasticsearch cleaner] {}'.format(es.wrapper.info()))
        hevlog.logging.debug('[elasticsearch cleaner] {}'.format(es.get_indices()))

        DAYS = 30

        pattern = '*'
        search = es.search_indices(pattern)
        keys = sorted(list(search.keys()))

        # ignore these indices
        keys.remove('.kibana')

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
        sleeper.day('elasticsearch cleanup')
