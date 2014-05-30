# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django import template
from django.template.context import RequestContext
import json

from www.lib import page, utils
from www.lib.decorators import request_limit_by_ip, member_required
from www.comment import interface


def format_outerobj_comment(objs, login_user):
    """
    @attention: 格式化
    """
    for obj in objs:
        # 删除标记
        obj.delete_flag = True if login_user.id else False
        obj.content = interface.replace_at_html(obj.content)
    return objs


def get_outerobj_comment(request):
    outerobj_type = request.POST.get('outerobj_type')
    outerobj_id = request.POST.get('outerobj_id')
    comment_show_type = request.POST.get('comment_show_type', 0)
    page_num = int(request.REQUEST.get('page', 1))
    # 能否发表评论权限判断
    can_create_comment_permission = request.POST.get('can_create_comment_permission', 'True')
    can_create_comment_permission = True if can_create_comment_permission == 'True' else False
    cob = interface.CommentOperateBase()
    objs = cob.get_outerobj_comment(outerobj_type, outerobj_id)

    # 分页
    page_objs = page.Cpt(objs, count=10, page=page_num).info
    objs = page_objs[0]
    page_params = (page_objs[1], page_objs[4])
    lst_comment = format_outerobj_comment(objs, request.user)

    from www.custom_tags.templatetags.custom_filters import paging
    from www.comment.interface import get_comment_page_onclick
    paging_html = paging(page_params, request, get_page_onclick=get_comment_page_onclick,
                         page_onclick_params=dict(outerobj_type=outerobj_type, outerobj_id=outerobj_id,
                                                  comment_show_type=comment_show_type,
                                                  can_create_comment_permission=can_create_comment_permission))

    # 两种类型,一种给用于单条外部对象,一条用于可能有多条的
    tem = template.loader.get_template('comment/_comment_sub%s.html' % comment_show_type)
    context_instance = RequestContext(request)
    context_instance.update(dict(lst_comment=lst_comment, outerobj_type=outerobj_type, outerobj_id=outerobj_id,
                                 request=request, paging_html=paging_html,
                                 can_create_comment_permission=can_create_comment_permission,
                                 comment_user=request.session.get('comment_user')))

    return HttpResponse(tem.render(template.Context(context_instance, autoescape=False)))


@request_limit_by_ip(200)
def add(request):
    """
    @attention: 发表评论
    """
    content = request.POST.get('content', '').strip()
    nick = request.POST.get('nick', '').strip()
    email = request.POST.get('email', '').strip()
    user_href = request.POST.get('user_href', '').strip()

    outerobj_type = request.POST.get('outerobj_type', 'default')
    outerobj_id = request.POST.get('outerobj_id')
    comment_show_type = request.POST.get('comment_show_type', 0)

    cob = interface.CommentOperateBase()
    flag, result = cob.add(nick, email, user_href, content, outerobj_type, outerobj_id, ip=utils.get_clientip(request))
    if flag:
        lst_comment = format_outerobj_comment([result, ], request.user)
        # 两种类型,一种给用于单条外部对象,一条用于可能有多条的
        tem = template.loader.get_template('comment/_comment_single_list%s.html' % comment_show_type)
        context_instance = RequestContext(request)
        context_instance.update(dict(c=lst_comment[0], outerobj_type=outerobj_type, outerobj_id=outerobj_id))

        # 设置留言用户session
        request.session['comment_user'] = dict(nick=nick, email=email, user_href=user_href)
        return HttpResponse(tem.render(template.Context(context_instance, autoescape=False)))
    else:
        return HttpResponse('$%s' % result)


@member_required
def remove(request):
    """
    @attention: 删除评论
    """
    user = request.user
    id = request.POST.get('id')

    cob = interface.CommentOperateBase()
    flag, result = cob.remove_comment(id, user)
    r = dict(flag='0' if flag else '-1', result=id if flag else result)
    return HttpResponse(json.dumps(r), mimetype='application/json')
