# -*- coding: utf-8 -*-

import json
import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from www.lib import utils, cache


class request_limit_by_ip(object):

    """
    @note: 根据ip地址限制操作次数
    """

    def __init__(self, max_count, cycle=3600 * 24):
        self.max_count = max_count
        self.cycle = cycle

    def __call__(self, func):
        def _decorator(request, *args, **kwargs):
            cache_key = u'%s_%s_%s' % (utils.get_function_code(func), utils.get_clientip(request),
                                       str(datetime.datetime.now().date()))
            cache_count = cache.get(cache_key, original=True)
            if cache_count is None:
                cache.set(cache_key, 1, time_out=self.cycle, original=True)
            else:
                cache_count = int(cache_count)
                cache_count += 1
                cache.incr(cache_key)
                if cache_count > self.max_count:
                    if request.is_ajax():
                        return HttpResponse(json.dumps(dict(flag=-1, result=u'request limited by ip')))
                    else:
                        return render_to_response('error.html', dict(err_msg=u'request limited by ip'),
                                                  context_instance=RequestContext(request))
            return func(request, *args, **kwargs)
        return _decorator


def member_required(func):
    def _decorator(request, *args, **kwargs):
        flag = False
        if hasattr(request, 'user') and request.user.is_authenticated():
            flag = True
        if not flag:
            if request.is_ajax():
                return HttpResponse('need_login')
            else:
                return HttpResponseRedirect("/error_info?err_msg=%s" % "this request need login")

        return func(request, *args, **kwargs)
    return _decorator
