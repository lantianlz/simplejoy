# -*- coding: utf-8 -*-

from main.lib import utils, cache
from main.blog.models import BlogRoll, FriendCheck, Essay, Category

dict_err = {
    101: u'已提交该博客的申请，审核中，请勿重复申请',
    102: u'这名字，不在博主好友列表中哦，无法显示电话号码',
    103: u'朋友，这名字真熟，但不是我好友哦',
    104: u'博客地址须已http://开头',
    105: u'唬我呢，什么邮箱格式!',
    106: u'虽然我很喜欢我自己，但是不要冒充我',

    000: u'成功',
    998: u'在某些框框里，该填的尚未填',
    999: u'系统错误',
}


def apply_blogroll(name, link, email, ip):
    '''
    @note: 提交博客申请
    '''
    try:
        assert all((name, link, email))
    except:
        return False, dict_err.get(998)

    if not (link.startswith('http://') or link.startswith('https://')):
        return False, dict_err.get(104)

    if not utils.vemail(email):
        return False, dict_err.get(105)

    if BlogRoll.objects.filter(link=link):
        return False, dict_err.get(101)

    BlogRoll.objects.create(name=name, link=link, email=email, ip=ip)
    e_content = u'博客名称为:%s, 链接为：%s\n联系方式为:%s, ip为：%s' % (name, link, email, ip)
    utils.send_email_to_me(title=u'收到一个信息博客友情链接请求', content=e_content)

    return True, dict_err.get(000)


def check_friend_name(name, ip):
    '''
    @note: 好友检测
    '''
    import re

    try:
        assert all((name, ip))
    except:
        return False, dict_err.get(998)

    p = re.compile(u'^[\u4e00-\u9fa5]{2,4}$', re.I)
    if not p.findall(name):
        return False, dict_err.get(102)

    if name in (u'张三', u'李四', u'王五', u'赵六', u'二百五'):
        return False, dict_err.get(103)

    if name == u'李政':
        return False, dict_err.get(106)

    FriendCheck.objects.get_or_create(name=name, defaults=dict(ip=ip))

    e_content = u'姓名为:%s, ip为：%s' % (name, ip)
    utils.send_email_to_me(title=u'收到一个显示电话号码的请求', content=e_content)

    return True, u'13005012270'


def get_valid_blogrolls():
    key = u'all_valid_blogroll'
    vbs = cache.get(key)
    if vbs is None:
        vbs = BlogRoll.objects.filter(state=True)
        cache.set(key, vbs)

    return vbs


def get_all_valid_catagory():
    key = u'all_category'
    cs = cache.get(key)
    if cs is None:
        cs = Category.objects.filter(state=True)
        cache.set(key, cs)
    return cs


def get_catagory_by_domain(category_domain):
    cs = get_all_valid_catagory()

    for c in cs:
        if c.domain == category_domain:
            return c


def get_all_essays():
    key = u'all_valid_essays'
    essays = cache.get(key)
    if essays is None:
        essays = Essay.objects.select_related('category').filter(state=True)
        cache.set(key, essays)
    return essays


def get_essays_by_category(category):
    essays = get_all_essays()
    c_essays = []
    if category:
        for e in essays:
            if e.category_id == category.id:
                c_essays.append(e)
    return c_essays


def format_essay_list_groupby_year(essays):
    dict_essays = {}
    for e in essays:
        year = e.create_time.strftime('%Y')
        if year in dict_essays:
            dict_essays[year].append(e)
        else:
            dict_essays[year] = [e, ]
    lst_essays = dict_essays.items()
    lst_essays.sort(key=lambda x: x[0], reverse=True)
    return lst_essays


def get_essay_by_id(id):
    all_valid_essays = get_all_essays()
    for essay in all_valid_essays:
        if str(id) == str(essay.id):
            return essay


def get_feeds():
    '''
    @note: 输出feeds供订阅使用
    '''
    import PyRSS2Gen
    import datetime

    rss = PyRSS2Gen.RSS2(title="simplejoy",
                         link="http://www.simplejoy.me",
                         description="this is simplejoy's blog, welcome and thank you for your visiting",
                         lastBuildDate=datetime.datetime.now(),
                         items=[PyRSS2Gen.RSSItem(title=essay.title,
                                                  link=essay.get_full_url(),
                                                  description=essay.content,
                                                  guid=PyRSS2Gen.Guid(essay.get_full_url()),
                                                  pubDate=essay.create_time) for essay in get_all_essays()[:20]],
                         )
    return rss.to_xml()


def get_kindly_msg(ip):
    '''
    @note: 获取首页温馨提醒
    '''
    import datetime
    import random
    lst_msgs = [
        {'type': 'time', 'msg': u'朋友，欢迎来访，夜已深，送你一首歌&nbsp;&nbsp;<a target="_blank" href="%s">%s</a>' %
         (
         (u'http://www.xiami.com/song/play?ids=/song/playlist/id/381755/object_name/default/object_id/0', u'想把我唱给你听'),
         (u'http://www.xiami.com/song/play?ids=/song/playlist/id/378730/object_name/default/object_id/0', u'她在睡梦中'),
         (u'http://v.youku.com/v_show/id_XODY5MDEzODg=.html', u'I am yours'),
         )
         [random.randint(0, 2)]},
    ]

    for msg in lst_msgs:
        if msg['type'] == 'time':
            cache_key = 'kindly_reminder_%s' % ip
            hour = int(datetime.datetime.utcnow().strftime('%H'))
            if (15 <= hour and hour <= 20) and cache.set_time_lock(cache_key, time_out=12 * 3600):
                return msg['msg']
