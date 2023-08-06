# -*- coding:utf-8 -*-

# @Time      :2023/6/17 14:03
# @Author    :huangkewei

import logging
from os import getenv

logger = logging.getLogger(__name__)


def get_env(env_name, default=None, required=False, arg_formatter=None):
    rv = getenv(env_name)
    if required and rv is None and default is None:
        raise ValueError("'{}' environment variable is required.".format(env_name))
    elif rv is None:
        logger.warning("'{}' uses default value: {}".format(env_name, default))
        rv = default
    if arg_formatter is not None:
        rv = arg_formatter(rv)
    return rv


REDIS_URL = get_env('REDIS_URL', 'redis://localhost:6379/0', required=True)
