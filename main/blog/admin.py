# -*- coding: utf-8 -*-

from django.contrib import admin

from main.blog.models import Essay, Category, BlogRoll, FriendCheck



class EssayAdmin(admin.ModelAdmin):
    list_display = ('title', 'auther_name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'domain')


class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'email')
    search_fields = ('name',)


class FriendCheckAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip')

admin.site.register(Essay, EssayAdmin)
admin.site.register(BlogRoll, BlogRollAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FriendCheck, FriendCheckAdmin)
