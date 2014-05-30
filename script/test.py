# -*- coding: utf-8 -*-

import sys
import os
sys.path.extend(['../../', 'e:\\workspace\\google_code\\simplejoy'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

from pprint import pprint
from www.lib import utils


def test_cache():
    from www.lib import cache
    key = 'test'
    value = 'test_value'

    print cache.set(key, value)
    print cache.get(key)
    # cache.flush()


def test_emalil():
    from www.lib import utils
    utils.send_email(emails="lizheng@codoon.com", title='test', content='test')


def test():
    from www.blog.interface import get_kindly_msg
    print get_kindly_msg('test').encode('utf8')


if __name__ == '__main__':
    # test_cache()
    # test_emalil()

    test()
