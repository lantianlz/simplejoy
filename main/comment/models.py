# -*- coding: utf-8 -*-

from django.db import models


outerobj_type_choices = ((0, u'essay'),)


class Comment(models.Model):

    """
    @attention:评论
    """
    nick = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    user_href = models.CharField(max_length=128, default='')
    content = models.CharField(max_length=512)
    outerobj_type = models.IntegerField(choices=outerobj_type_choices)  # 被评论对象类型
    outerobj_id = models.CharField(max_length=64, default=0)  # 被评论对象id
    author_readed = models.BooleanField(default=False)
    ip = models.IPAddressField()
    create_time = models.DateTimeField()

    def __unicode__(self):
        return self.content[:10]

    def type_show(self):
        """
        @attention: 获取类型的展现
        """
        outerobj_type_display = {'0': u'随笔', }
        return outerobj_type_display.get(str(self.outerobj_type))


class CommentCount(models.Model):

    """
    @attention: 评论数
    """
    outerobj_type = models.IntegerField(choices=outerobj_type_choices)  # 被评论对象类型
    outerobj_id = models.CharField(max_length=64, default=0)  # 被评论对象id
    count = models.IntegerField(default=0)
    update_time = models.DateTimeField()

    class Meta:
        unique_together = [('outerobj_type', 'outerobj_id')]

