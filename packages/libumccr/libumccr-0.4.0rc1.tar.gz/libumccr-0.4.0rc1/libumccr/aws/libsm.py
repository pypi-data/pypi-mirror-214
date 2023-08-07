# -*- coding: utf-8 -*-
"""libsm module

Module interface with AWS Secrets Manager and, LRU cache for hit less to AWS endpoint if any
"""
import base64
import logging

from cachetools.func import lru_cache

from libumccr.aws import sm_client

logger = logging.getLogger(__name__)


@lru_cache(maxsize=64)
def get_secret(secret_name):
    """
    If you are in long-running process and querying rotating value from secret manager such as JWT token, you may
    clear the cache before get secret call. e.g.

        libumccr.aws.libsm.get_secret.cache_clear()

    See https://github.com/umccr/gridss-purple-linx-nf/pull/25/files

    :param secret_name:
    :return:
    """
    resp = sm_client().get_secret_value(
        SecretId=secret_name
    )

    if 'SecretString' in resp:
        return resp['SecretString']
    else:
        return base64.b64decode(resp['SecretBinary'])
