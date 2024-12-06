import logging
from hcs_core.sglib.client_util import hdc_service_client

log = logging.getLogger(__name__)

_client = hdc_service_client("scm")


def health():
    return _client.get("/v1/health")
