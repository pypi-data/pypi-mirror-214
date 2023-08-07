import logging
import uuid
from typing import List

from libumccr import libjson
from libumccr.aws import eb_client

logger = logging.getLogger(__name__)

MAX_BATCH_SIZE = 10


def get_event_buses(**kwargs):
    """Proxy to
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/list_event_buses.html

    :param kwargs:
    :return:
    """
    return eb_client().list_event_buses(**kwargs)


def emit_events(entries: List[dict]) -> dict:
    """Proxy to
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/client/put_events.html

    :param entries:
    :return:
    """
    return eb_client().put_events(Entries=entries)


def emit_event(entry: dict) -> dict:
    return emit_events([entry])


def dispatch_events(entries: List[dict], batch_size=10):
    """
    PutEvents has maximum number of 10 entries per API call. So, this function batch them up if more than 10 entries.
    https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html

    :param entries:
    :param batch_size:
    :return:
    """
    _batch_size = batch_size if batch_size < MAX_BATCH_SIZE else MAX_BATCH_SIZE
    _chunks = [entries[x:x + _batch_size] for x in range(0, len(entries), _batch_size)]
    responses = {}
    for chunk in _chunks:
        chunk_id = str(uuid.uuid4())
        resp = emit_events(chunk)
        responses[chunk_id] = resp

    logger.info(f"EVENT BUS RESPONSE: \n{libjson.dumps(responses)}")
    return responses
