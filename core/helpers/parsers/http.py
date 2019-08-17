from core.helpers.neo4j import helpers
# from core.helpers import crypto


def http_header(headers):
    # [print(x) for x in auth.request_headers(request)]

    # token = crypto.hash_key(sorted([x for x in headers]))

    args = dict(
        blob=sorted(headers),
        label='Headers'
    )

    helpers.prepare_dict(**args)
