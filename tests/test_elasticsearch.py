from core.helpers.elasticsearch import ElasticsearchConnect


def test_ElasticsearchConnect():
    assert ElasticsearchConnect(['elasticsearch.0000000'], use_ssl=False, request_timeout=1).wrapper.ping() is False
