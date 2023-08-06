# -*- coding:utf-8 -*-

# @Time      :2023/6/15 19:37
# @Author    :huangkewei

import random
import string
import redis
import logging
from .lock import Lock
from .lua_script import token_limit_script_with_add, token_limit_script, time_window_limit_script,\
    semaphore_limit_script, desemaphore_limit_script
from .conf import REDIS_URL

logger = logging.getLogger(__name__)


def generate_random_string(length):
    # 生成包含所有字母和数字的字符集
    characters = string.ascii_letters + string.digits
    # 从字符集中随机选择 length 个字符
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string


class TokenLimit:
    def __init__(self, capacity, interval, url=REDIS_URL):
        """

        :param capacity: 令牌桶大小
        :param interval: 时间间隔
        :param url: redis链接
        """
        self.capacity = capacity
        self.interval = interval
        self.rate = round(capacity/interval, 5)

        self.lock = Lock(url)
        self.redis = self.lock.redis
        # self.redis = redis.from_url(url=url)
        self.token_limit_script_with_add = self.redis.script_load(token_limit_script_with_add)
        self.token_limit_script = self.redis.script_load(token_limit_script)

    def get_token(self, key):
        """
        获取令牌

        :param key: 令牌桶名称key
        :return:
        """
        token_key = 'token_' + key

        lock_key = 'lock_' + key
        random_str = generate_random_string(16)
        lock_status = self.lock.acquire(lock_key, random_str, immediately=True)
        if lock_status:
            logger.info('获取到添加令牌权限，获取并添加令牌。')

            token_status = self.redis.evalsha(self.token_limit_script_with_add, 1, token_key,
                               self.capacity, self.rate)
            self.lock.release(lock_key, random_str)
        else:
            logger.info('未获取到添加令牌权限，只进行获取令牌。')
            token_status = self.redis.evalsha(self.token_limit_script, 1, token_key)

        if token_status:
            logger.info('成功获取到令牌.')
        else:
            logger.info('获取令牌失败.')

        return token_status

    def __call__(self, key):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    token_status = self.get_token(key)
                    if token_status:
                        return func(*args, **kwargs)
                    else:
                        raise Exception('获取令牌失败，暂无可用令牌')
                except Exception as e:
                    # todo 重试连接redis服务
                    raise e

            return _wrapper

        return _decorator


class TimeWindowLimit:
    def __init__(self, limit, window, url=REDIS_URL):
        self.limit = limit
        self.window = window
        self.redis = redis.from_url(url=url)
        self.time_window = self.redis.script_load(time_window_limit_script)

    def get_status(self, key):
        for _ in range(3):
            time_window_key = 'time_window_' + key
            status = self.redis.evalsha(self.time_window, 1, time_window_key,
                                        self.limit, self.window)
            if status != 2:
                return status
            continue
        return 0

    def __call__(self, key):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    status = self.get_status(key)
                    if status:
                        return func(*args, **kwargs)
                    else:
                        raise Exception('时间窗口: 此时间窗口限流中。')
                except Exception as e:
                    # todo 重试连接redis服务
                    raise e

            return _wrapper

        return _decorator


class SemaphoreLimit:
    def __init__(self, limit, expire_time, url=REDIS_URL):
        self.limit = limit
        self.expire_time = expire_time
        self.redis = redis.from_url(url=url)
        self.semaphore = self.redis.script_load(semaphore_limit_script)
        self.desemaphore = self.redis.script_load(desemaphore_limit_script)

    def acquire(self, key):
        semaphore_key = 'semaphore_' + key
        status = self.redis.evalsha(self.semaphore, 1, semaphore_key,
                                    self.limit, self.expire_time)
        return status

    def release(self, key):
        semaphore_key = 'semaphore_' + key
        status = self.redis.evalsha(self.desemaphore, 1, semaphore_key,
                                    self.expire_time)
        return status

    def __call__(self, key):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    status = self.acquire(key)
                    if status:
                        res = func(*args, **kwargs)
                        self.release(key)
                        return res
                    else:
                        raise Exception('获取信号量失败，暂无可用的信号量')
                except Exception as e:
                    # todo 重试连接redis服务
                    raise e

            return _wrapper

        return _decorator


class Limit:
    def __init__(self, limit_info):
        if len(limit_info)<1:
            raise Exception('限流器参数太少！')

        self.limit_map = {
            'token': TokenLimit,
            'time_window': TimeWindowLimit,
            'semaphore': SemaphoreLimit
        }
        if isinstance(limit_info[0], (list, tuple)):
            self.limit_decorators = []
            limit_info = limit_info[::-1]
            for one_limit in limit_info:
                limit_type = one_limit[0]
                LimitClass = self.get_limit_map(limit_type)
                self.limit_decorators.append(LimitClass(*one_limit[1:]))
        else:
            limit_type = limit_info[0]
            LimitClass = self.get_limit_map(limit_type)
            self.limit_decorators = [LimitClass(*limit_info[1:])]

    def gen_decorator_func(self, key, func):
        decorator_func = func
        for one_decorator in self.limit_decorators:
            decorator_func = one_decorator(key)(decorator_func)

        return decorator_func

    def get_limit_map(self, limit_type):
        LimitClass = self.limit_map.get(limit_type)
        if LimitClass is None:
            raise Exception('没有对应的限流方式！')
        return LimitClass

    def __call__(self, key):
        def _decorator(func):
            def _wrapper(*args, **kwargs):
                try:
                    return self.gen_decorator_func(key, func)(*args, **kwargs)
                except Exception as e:
                    # todo 重试连接redis服务
                    raise e

            return _wrapper

        return _decorator




