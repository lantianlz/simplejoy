# -*- coding: utf-8 -*-
"""
@note: 自定义标签文件
@author: lizheng
"""
import datetime
# from django.http import HttpResponse
# from django.template.context import RequestContext
from django import template
register = template.Library()


@register.simple_tag
def current_time(format_string):
    """
    @note: 当前时间tag
    """
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag(takes_context=True)
def import_variable(context, name, value, json_flag=False):
    """
    @note: 传入一个变量到context中
    """
    from django.utils.encoding import smart_str
    import json
    value = smart_str(value)
    context[name] = value if not json_flag else json.loads(value)
    return ''


@register.simple_tag(takes_context=True)
def display_nav_category(context):
    """
    @note: 导航中的分类展现
    """
    from main.blog.interface import get_all_valid_catagory
    cs = get_all_valid_catagory()

    html = u''
    for c in cs:
        html += u'<li><a href="%s" title="%s">%s</a></li>' % (c.get_url(), c.title, c.name)
    return html


    # tem = template.loader.get_template('includes/_global_notification.html')
    # context_instance = RequestContext(request)
    # context_instance.update(dict(notifications=notifications))
    # return tem.render(template.Context(context_instance, autoescape=context.autoescape))
