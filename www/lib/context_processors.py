# -*- coding: utf-8 -*-

"""
@attention: 定义全局上下文变量
@author: lizheng
@date: 2011-11-28
"""

from django.conf import settings


def config(request):
    """
    @attention: Adds settings-related context variables to the context.
    """
    import random
    import datetime

    return {
        'DEBUG': settings.DEBUG,
        'RSS_IMG': random.randint(2, 5),
        'MEDIA_VERSION': settings.MEDIA_VERSION,
        'LOCAL_FLAG': settings.LOCAL_FLAG,
        'YEAR': datetime.datetime.now().strftime("%Y")
    }
