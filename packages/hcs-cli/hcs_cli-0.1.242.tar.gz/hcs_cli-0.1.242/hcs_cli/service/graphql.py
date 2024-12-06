import logging
from hcs_core.sglib.client_util import hdc_service_client

log = logging.getLogger(__name__)

_client = None


def post(payload: dict):
    global _client
    if _client is None:
        _client = hdc_service_client("graphql")
    return _client.post("/", json=payload)
