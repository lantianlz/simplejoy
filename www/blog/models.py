# -*- coding: utf-8 -*-

from django.db import models


class Essay(models.Model):
    source_choices = ((0, u'本博客'), (1, u'人人网'), (2, u'QQ空间'))
    title = models.CharField(max_length=128, unique=True)
    content = models.TextField()
    source = models.IntegerField(default=0, choices=source_choices)                             # 来源
    outer_link = models.CharField(max_length=128, default='#')                                   # 站外链接
    auther_name = models.CharField(max_length=32, default='simplejoy')
    auther_url = models.CharField(max_length=128, default='#')
    category = models.ForeignKey('Category')

    pv = models.IntegerField(default=0)
    uv = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    sort_num = models.IntegerField(default=100, db_index=True)
    state = models.BooleanField(default=True)
    create_time = models.DateTimeField()

    class Meta:
        ordering = ['-create_time']

    def __unicode__(self):
        return self.title

    def get_url(self):
        return u'/essay/%s' % self.id

    def get_full_url(self):
        '''
        @note: 给rss输出使用
        '''
        from django.conf import settings
        return u'http://www.%s%s' % (settings.SITE_DOMAIN, self.get_url())


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=256, default='')
    domain = models.CharField(max_length=16, unique=True, default='1')
    sort_num = models.IntegerField(default=100, db_index=True)
    state = models.BooleanField(default=True, db_index=True)
    data_body = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['sort_num', ]

    def __unicode__(self):
        return self.name

    def get_url(self):
        return u'/c/%s' % self.domain


class BlogRoll(models.Model):
    btype_choices = ((0, u'默认'), (1, u'认识朋友'))
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=64, unique=True)
    email = models.CharField(max_length=64)
    btype = models.IntegerField(default=0, choices=btype_choices)
    ip = models.IPAddressField()
    state = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.link


class FriendCheck(models.Model):
    ip = models.IPAddressField()
    name = models.CharField(max_length=32, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)


class IpConfig(models.Model):
    ip = models.IPAddressField()
    count = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now_add=True)
