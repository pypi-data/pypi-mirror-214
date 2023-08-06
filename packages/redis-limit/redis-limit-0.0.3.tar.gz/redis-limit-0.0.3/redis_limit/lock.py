# -*- coding:utf-8 -*-

# @Time      :2023/6/15 16:15
# @Author    :huangkewei

import time
import redis
import logging
from .conf import REDIS_URL

logger = logging.getLogger(__name__)

# 分布式加锁
lock_script = """
local key = KEYS[1]
local value = ARGV[1]
local ex_value = ARGV[2]
return redis.call('set', key, value, 'ex', ex_value, 'nx')
"""

# 分布式解锁
unlock_script = """
local key = KEYS[1]
local value = ARGV[1]
if redis.call('get', key) == value then 
    return redis.call('del', key) 
else 
    return 0 
end
"""


class Lock:
    def __init__(self, url=REDIS_URL):
        self.redis = redis.from_url(url=url)
        self.lock_script = self.redis.script_load(lock_script)
        self.unlock_script = self.redis.script_load(unlock_script)

    def acquire(self, key, value, timeout=5, immediately=False):
        """
        获取锁

        # todo immediately 将immediately设置为函数执行时间，若加锁超时，则返回Fasle
        :param key:
        :param value:
        :param timeout:
        :param immediately:
        :return:
        """

        while True:
            lock_status = self.redis.evalsha(self.lock_script, 1, key, value, timeout)
            if lock_status is None:
                # 立即返回数据
                if immediately:
                    return False

                time.sleep(0.1)
                logger.debug(f'lock {key}:{value} fail. wait 0.1s.')
                continue

            logger.info(f'lock {key}:{value} success.')
            return True

    def release(self, key, value):
        """
        释放锁

        :param key:
        :param value:
        :return:
        """
        unlock_status = self.redis.evalsha(self.unlock_script, 1, key, value)
        if unlock_status == 0:
            logger.info(f'unlock fail. {key}:{value} no find.')
            return False
        else:
            logger.info(f'unlock {key}:{value} success.')
            return True

    def __call__(self, key, value, timeout=5, immediately=False):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    lock_status = self.acquire(key, value, timeout, immediately)
                    if lock_status:
                        res = func(*args, **kwargs)
                        self.release(key, value)
                        return res
                    else:
                        raise Exception('加锁失败')
                except Exception as e:
                    # todo 重试连接redis服务
                    raise e

            return _wrapper

        return _decorator

