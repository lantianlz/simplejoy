# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
from www.lib import debug, utils
import logging


class ErrorInfoMidware(object):

    def __init__(self):
        pass

    def process_exception(self, request, exception):
        if type(exception) == Http404:
            return
        info = debug.get_debug_detail(exception)
        url = request.path
        params = "\n".join(["".join([k, request.REQUEST.get(k)]) for k in request.REQUEST])
        content = "request path=%s \n------------------------------------\n%s\n---------------------------------------------\nparams:\n%s" % (url, info, params)
        title = u"blog %s error %s in %s" % (settings.SERVER_NAME, exception, url)
        logging.error(title + "\n" + content)
        if not settings.DEBUG:
            utils.send_email_to_me(title, content, async=False, type="text")
