from core.helpers.elasticsearch import ElasticsearchWrapper


def test_ElasticsearchWrapper():
    assert ElasticsearchWrapper(['elasticsearch.0000000'], use_ssl=False, request_timeout=1).connected is False
