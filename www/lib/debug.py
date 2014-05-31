# -*- coding: utf-8 -*-

"""
@attention: 调试信息获取、打印
@author: lizheng
@date: 2011-11-28
"""

import sys
import traceback
import datetime
from django.utils.encoding import smart_unicode


def print_debug_info(e):
    if True:
        from logging import log, ERROR
        now = datetime.datetime.now()
        log(ERROR, u'%s%s' % ('1' * 50, 'global_debug_info'))
        log(ERROR, now)
        log(ERROR, get_debug_info(e))


def get_debug_info(e):
    errorMeg = u'%s\n' % e
    for file, lineno, function, text in traceback.extract_tb(sys.exc_info()[2]):
        errorMeg += u'%s, in %s\n%s:                %s!\n' % (file, function, lineno, text)
    return u"blog error -%s" % errorMeg


class Frame(object):

    def __init__(self, tb):
        self.tb = tb
        frame = tb.tb_frame
        self.locals = {}
        self.locals.update(frame.f_locals)

    def print_path(self):
        return smart_unicode(traceback.format_tb(self.tb, limit=1)[0])

    def print_local(self):
        return u"\n".join(["%s=%s" % (k, self.dump_value(self.locals[k])) for k in self.locals])

    def dump_value(self, v):
        try:
            return smart_unicode(str(v))
        except:
            return u"value can not serilizable"


def get_debug_detail(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    frames = []
    tb = exc_traceback
    frames.append(tb.tb_frame)
    detail = u"blog error -Exception:%s\n" % e
    while tb.tb_next:
        tb = tb.tb_next
        fm = Frame(tb)
        detail += fm.print_path()
        detail += u"\nlocals variables:\n"
        detail += fm.print_local()
        detail += u"\n-------------------------------------------------------\n"
    return detail


def log_debug_detail(e):
    from django.conf import settings
    import logging
    msg = get_debug_detail(e)
    logging.error(msg)

    if not settings.DEBUG:
        from www.lib import utils
        utils.send_email_to_me(title='blog error', content=msg)