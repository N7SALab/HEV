from core.helpers.neo4j import helpers


def http_header(headers):
    # [print(x) for x in auth.request_headers(request)]

    # token = helper_brain.hash_key(sorted([x for x in headers]))

    args = dict(
        blob=sorted(headers),
        label='Headers'
    )

    helpers.prepare_dict(**args)
