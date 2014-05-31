# -*- coding: utf-8 -*-

from django.utils.encoding import smart_str

import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=1)


def get(key):
    key = smart_str(key)
    return mc.get(key)


def set(key, value, time_out=0):
    key = smart_str(key)
    if time_out:
        mc.set(key, value, time=time_out)
    else:
        mc.set(key, value)


def delete(key):
    key = smart_str(key)
    mc.delete(key)


def incr(key, delta=1):
    key = smart_str(key)
    return mc.incr(key, delta)


def decr(key, delta=1):
    key = smart_str(key)
    return mc.decr(key, delta)


def flush():
    mc.flush_all()

if __name__ == '__main__':
    import sys
    import os
    sys.path.extend(['../../', 'e:\\workspace\\google_code\\simplejoy'])
    os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

    print mc.flush_all()
