# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'main.blog.views.essay_index'),
                       url(r'^about$', 'main.blog.views.about'),
                       url(r'^blogroll$', 'main.blog.views.blogroll'),
                       url(r'^c/(?P<category_domain>\w+)$', 'main.blog.views.category_essay'),
                       url(r'^advert$', 'main.blog.views.advert'),
                       url(r'^essay/(?P<id>[\w\-\_]+)$', 'main.blog.views.essay_detail'),
                       url(r'^feed$', 'main.blog.views.feed'),
                       url(r'^500$', 'main.blog.views.touch500'),
                       url(r'^error_info$', 'main.blog.views.error_info'),

                       url(r'^comment/', include('main.comment.urls')),
                       url(r'^s/(?P<template_name>.*)$', 'main.blog.views.static'),
                       # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                       #     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )


# ajax部分
urlpatterns += patterns('',
                        url(r'^apply_blogroll$', 'main.blog.views.apply_blogroll'),
                        url(r'^check_friend_name$', 'main.blog.views.check_friend_name'),
                        )
