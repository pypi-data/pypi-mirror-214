# -*- coding:utf-8 -*-

# @Time      :2023/6/15 19:51
# @Author    :huangkewei

def modifier1(func):
    def wrapper():
        print("Before func")
        func()
        print("After func")
    return wrapper

def modifier2(func):
    def wrapper():
        print("Before func 2")
        func()
        print("After func 2")
    return wrapper

# @modifier1
# @modifier2
def my_func():
    print("Hello, world!")

my_func = modifier1(modifier2(my_func))


