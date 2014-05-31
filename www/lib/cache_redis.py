# -*- coding: utf-8 -*-

import redis
from cPickle import dumps, loads


cache_config = ('127.0.0.1', 6379, 5)
pool = redis.ConnectionPool(host=cache_config[0], port=cache_config[1], db=cache_config[2])
conn = redis.Redis(connection_pool=pool)


def get(key, original=False):
    '''
    @note: original表示是否是保存原始值，用于incr这样的情况
    '''
    obj = conn.get(key)
    if obj:
        return loads(obj) if not original else obj
    return None


def set(key, value, time_out=0, original=False):
    s_value = dumps(value) if not original else value
    if time_out:
        if conn.exists(key):
            conn.setex(key, s_value, time_out)
        else:
            conn.setnx(key, s_value)
            conn.expire(key, time_out)
    else:
        conn.set(key, s_value)


def delete(key):
    return conn.delete(key)


def incr(key, delta=1):
    return conn.incrby(key, delta)


def decr(key, delta=1):
    return conn.decr(key, delta)


def exists(key):
    return conn.exists(key)


def set_time_lock(key, time_out):
    '''
    @note: 设置锁定时间
    '''
    key = "tlock:%s" % key
    if conn.exists(key):
        return False
    conn.set(key, 0, time_out)
    return True


def flush():
    conn.flushdb()


if __name__ == '__main__':
    import sys
    import os
    sys.path.extend(['../../', 'e:\\workspace\\google_code\\simplejoy'])
    sys.path.extend(['../../', 'f:\\workspace\\googlecode\\simplejoy'])
    os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

    # print incr('add_127.0.0.1_2013-09-15', 1)
    # print decr('a', 3)
    # from pprint import pprint
    # pprint(dir(conn))

    print set_time_lock('key', time_out=10)
