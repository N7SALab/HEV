import datetime
import elasticsearch

from elasticsearch import Elasticsearch, RequestsHttpConnection

from core.helpers.log import hevlog


hevlog = hevlog(level='debug')


class ElasticsearchConnect:

    def __init__(self, host=['elasticsearch'], port=9200, request_timeout=10,
                 http_auth=None, use_ssl=True, verify_certs=True,
                 connection_class=RequestsHttpConnection):
        for _host in host:
            try:
                # TODO: maybe make this accept only one host
                self.wrapper = Elasticsearch(
                    hosts=[{'host': _host, 'port': port}],
                    request_timeout=request_timeout,
                    http_auth=http_auth,
                    use_ssl=use_ssl,
                    verify_certs=verify_certs,
                    connection_class=connection_class
                )
            except:
                self.wrapper = None
            finally:
                if self.wrapper is None:
                    raise Exception('No elasticsearch hosts available')

        self.host = host
        self.port = port
        self.cache = []
        self.indices = []

    def search_indices(self, index_pattern):
        try:
            retrieved_indices = self.wrapper.indices.get(index_pattern)
            num_indices = len(retrieved_indices)

            msg = 'Search found {} indices'
            msg = msg.format(num_indices)
            hevlog.log(msg, self.search_indices.__name__, 'info')
            return retrieved_indices
        except elasticsearch.exceptions.NotFoundError:
            msg = '''You provided the index pattern '{}', but searches returned fruitless'''
            msg = msg.format(index_pattern)
            hevlog.log(msg, self.search_indices.__name__, 'error')

    def delete_indices(self, index_pattern):

        retrieved_indices = [x for x in self.search_indices(index_pattern).keys()]
        num_indices = len(retrieved_indices)

        msg = 'Search found {} indices'
        msg = msg.format(num_indices)
        hevlog.log(msg, self.delete_indices.__name__, 'info')

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
        msg = 'Retrieved {} indices'
        msg = msg.format(num_indices)
        hevlog.log(msg, self.get_indices.__name__, 'info')


async def run(event_loop, CONF):

    while True:
        es = ElasticsearchConnect(CONF['hosts'], use_ssl=False, request_timeout=40)

        hevlog.log(es.wrapper.info(), run.__name__, 'debug')
        hevlog.log(es.get_indices(), run.__name__, 'debug')

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
                print('deleted', alias)

        print('done')
