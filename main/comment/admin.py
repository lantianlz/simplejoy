# -*- coding: utf-8 -*-

from django.contrib import admin

from main.comment.models import Comment, CommentCount


class CommentAdmin(admin.ModelAdmin):
    list_display = ('nick', 'email')


class CommentCountAdmin(admin.ModelAdmin):
    list_display = ('outerobj_id', 'count')


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentCount, CommentCountAdmin)
