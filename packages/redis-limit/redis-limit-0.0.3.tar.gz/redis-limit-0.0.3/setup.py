# -*- coding:utf-8 -*-

# @Time      :2022/10/21 14:26
# @Author    :huangkewei

import setuptools

setuptools.setup(
    name='redis-limit',
    version='0.0.3',
    author='huangkewei',
    description='基于redis的限流器以及锁',
    packages=setuptools.find_packages(),
    install_requires=[
        'redis>=4.4.0',
    ]
)

