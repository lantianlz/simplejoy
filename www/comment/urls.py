# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('www.comment.views',
                      (r'^get_outerobj_comment$', 'get_outerobj_comment'),
                      (r'^add$', 'add'),
                      (r'^remove$', 'remove'),
                       )
