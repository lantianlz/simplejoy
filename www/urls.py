# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'www.blog.views.essay_index'),
                       url(r'^about$', 'www.blog.views.about'),
                       url(r'^blogroll$', 'www.blog.views.blogroll'),
                       url(r'^c/(?P<category_domain>\w+)$', 'www.blog.views.category_essay'),
                       url(r'^advert$', 'www.blog.views.advert'),
                       url(r'^essay/(?P<id>[\w\-\_]+)$', 'www.blog.views.essay_detail'),
                       url(r'^feed$', 'www.blog.views.feed'),
                       url(r'^500$', 'www.blog.views.touch500'),
                       url(r'^error_info$', 'www.blog.views.error_info'),

                       url(r'^comment/', include('www.comment.urls')),
                       url(r'^s/(?P<template_name>.*)$', 'www.blog.views.static'),
                       # url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                       #     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )


# ajax部分
urlpatterns += patterns('',
                        url(r'^apply_blogroll$', 'www.blog.views.apply_blogroll'),
                        url(r'^check_friend_name$', 'www.blog.views.check_friend_name'),
                        )
