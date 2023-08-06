# -*- coding:utf-8 -*-

# @Time      :2023/6/15 19:35
# @Author    :huangkewei

# 获取信号量
semaphore_limit_script = """
local key = KEYS[1] -- Redis键名
local limit = tonumber(ARGV[1]) -- 限流器阈值
local expire_time = tonumber(ARGV[2]) -- Redis键过期时间
local count = tonumber(redis.call('GET', key) or "0") -- 当前计数器值

if count + 1 > limit then -- 如果超过了阈值
    return 0
else
    redis.call('INCRBY', key, 1) -- 计数器加1
    redis.call('EXPIRE', key, expire_time) -- 设置过期时间
    return 1
end
"""

# 释放信号量
desemaphore_limit_script = """
local key = KEYS[1] -- Redis键名
local expire_time = tonumber(ARGV[1]) -- Redis键过期时间
local count = tonumber(redis.call('GET', key) or "0") -- 当前计数器值

if count - 1 < 0 then -- 如果超过了阈值
    return 0
else
    redis.call('DECRBY', key, 1) -- 计数器减1
    redis.call('EXPIRE', key, expire_time) -- 设置过期时间
    return 1
end
"""

# 时间窗口
time_window_limit_script = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2]) * 1000

local now_lst = redis.call('time')
local now_str = now_lst[1]..string.sub(now_lst[2], 1, 3)
local now = tonumber(now_str)

redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)

local count = redis.call('ZCARD', key)

if count < limit then
    local zadd_status = redis.call('ZADD', key, 'NX', now, now)
    if zadd_status == 1 then
        return 1
    else
        return 2
    end
else
    return 0
end
"""

# 获取令牌，并添加令牌
token_limit_script_with_add = """
-- 获取当前时间戳
local now = tonumber(redis.call('time')[1])

-- 获取令牌桶中的令牌数量和最后更新时间戳
local result = redis.call('hmget', KEYS[1], 'tokens', 'last_refreshed')

local tokens = tonumber(result[1])
local last_refreshed = tonumber(result[2])
-- redis.log(redis.LOG_WARNING, tokens)

if tokens == nil then 
    redis.call('hmset', KEYS[1], 'tokens', 0, 'last_refreshed', now)
    tokens = 0
    last_refreshed = now
end

-- 计算令牌桶中应该有的令牌数量
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local expected_tokens = math.min(capacity, tokens + (now - last_refreshed) * rate)

-- 判断是否可以通过限流器
if expected_tokens < 1 then
    return 0
else
    -- 更新令牌桶中的令牌数量和最后更新时间戳
    redis.call('hmset', KEYS[1], 'tokens', expected_tokens - 1, 'last_refreshed', now)
    return 1
end
"""

# 只获取令牌
token_limit_script = """
-- 获取当前时间戳
local now = tonumber(redis.call('time')[1])

-- 获取令牌桶中的令牌数量和最后更新时间戳
local result = redis.call('hmget', KEYS[1], 'tokens', 'last_refreshed')

local tokens = tonumber(result[1])
if tokens == nil then 
    tokens = 0
end

-- 判断是否可以通过限流器
if tokens < 1 then
    return 0
else
    -- 更新令牌桶中的令牌数量
    redis.call('hmset', KEYS[1], 'tokens', tokens - 1)
    return 1
end
"""
