# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response  # , HttpResponseRedirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
import json

from www.lib import utils
from www.lib.decorators import request_limit_by_ip
from www.blog import interface


def essay_index(request, template_name='essay_index.html'):
    """
    @note: 首页
    """
    user_agent = utils.get_agent(request.META.get('HTTP_USER_AGENT'))
    if user_agent in ('ie6', ) and request.GET.get('ignoreie6') is None:
        return render_to_response('bad_ie.html', locals(), context_instance=RequestContext(request))

    essays = interface.format_essay_list_groupby_year(interface.get_all_essays())
    kindly_msg = interface.get_kindly_msg(utils.get_clientip(request))
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def static(request, template_name):
    """
    @note: 静态模板渲染
    """
    try:
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))
    except:
        raise Http404


def about(request, template_name="about.html"):
    """
    @note: 关于我
    """
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def blogroll(request, template_name="blogroll.html"):
    """
    @note: 友情链接
    """
    vbs = interface.get_valid_blogrolls()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def category_essay(request, category_domain, template_name="essay_index.html"):
    """
    @note: 分类文章
    """
    category = interface.get_catagory_by_domain(category_domain)
    essays = interface.format_essay_list_groupby_year(interface.get_essays_by_category(category))
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def advert(request, template_name="advert.html"):
    """
    @note: 广告
    """
    from www.lib.consts import lst_advert_info
    return render_to_response(template_name, dict(lst_advert_info=lst_advert_info), context_instance=RequestContext(request))


def essay_detail(request, id, template_name="essay_detail.html"):
    """
    @note: 随笔详情
    """
    essay = interface.get_essay_by_id(id)
    if not essay:
        raise Http404
    outerobj_id = essay.id
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def feed(request):
    """
    @note: 输出rss订阅
    """
    feeds = interface.get_feeds()
    return HttpResponse(feeds, mimetype='text/xml')


def touch500(request):
    raise Exception(u'500 test')


def error_info(request, template_name="error.html"):
    err_msg = request.GET.get('err_msg')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# ajax###########################################################################################
@request_limit_by_ip(200)
def apply_blogroll(request):
    name = request.POST.get('blogroll_name', '').strip()
    link = request.POST.get('blogroll_link', '').strip()
    email = request.POST.get('blogger_email', '').strip()
    ip = utils.get_clientip(request)

    flag, result = interface.apply_blogroll(name=name, link=link, email=email, ip=ip)
    r = dict(flag='0' if flag else '-1', result=result)
    return HttpResponse(json.dumps(r), mimetype='application/json')


@request_limit_by_ip(200)
def check_friend_name(request):
    friend_name = request.POST.get('friend_name', '').strip()
    ip = utils.get_clientip(request)

    flag, result = interface.check_friend_name(name=friend_name, ip=ip)
    r = dict(flag='0' if flag else '-1', result=result)
    return HttpResponse(json.dumps(r), mimetype='application/json')
