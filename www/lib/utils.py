# -*- coding: utf-8 -*-

import re


def find_mention(text):
    regex = r'@(\w+)\s'
    return re.findall(regex, text)


def force_int(num, default=1):
    try:
        return int(num)
    except:
        return default


def create_random_str(length=16, confusing=True):
    """
    @attention: 生成随机字符串,去掉 0,o,O,1,l,
    """
    from random import choice
    if not confusing:
        chars = ('23456789'
                 'abcdefghijkmnpqrstuvwxyz'
                 'ABCDEFGHIJKLMNPQRSTUVWXYZ')
    else:
        chars = ('123456789'
                 'abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    salt = ''.join([choice(chars) for i in range(length)])
    return salt


def get_agent(user_agent):
    """
    @attention: 从请求中获取浏览器类型
    """
    user_agent = str(user_agent).lower()
    agent = 'unknown'
    if user_agent.find('msie') > -1 and user_agent.find('opera') == -1:
        agent = 'ie%s' % user_agent[user_agent.find('msie') + 5:user_agent.find('msie') + 6]
    elif user_agent.find('360') > -1:
        agent = '360'
    elif user_agent.find('gecko/') > -1:
        agent = 'gecko'
    elif user_agent.find('opera') > -1:
        agent = 'opera'
    elif user_agent.find('konqueror') > -1:
        agent = 'konqueror'
    elif user_agent.find('ipod') > -1:
        agent = 'ipod'
    elif user_agent.find('ipad') > -1:
        agent = 'ipad'
    elif user_agent.find('iphone') > -1:
        agent = 'iphone'
    elif user_agent.find('chrome/') > -1:
        agent = 'chrome'
    elif user_agent.find('applewebkit/') > -1:
        agent = 'safari'
    elif user_agent.find('googlebot/') > -1:
        agent = 'googlebot'
    elif user_agent.find('msnbot') > -1:
        agent = 'msnbot'
    elif user_agent.find('yahoo! slurp') > -1:
        agent = 'yahoobot'
    elif user_agent.find('mozilla/') > -1:
        agent = 'gecko'

    return agent


def send_email(emails, title, content, type='text'):
    from django.conf import settings
    from django.core.mail import send_mail, EmailMessage

    if not emails:
        return

    if not isinstance(emails, (list, tuple)):
        emails = [emails, ]

    if type != 'html':
        send_mail(title, content, settings.EMAIL_FROM, emails, fail_silently=True)
    else:
        msg = EmailMessage(title, content, settings.EMAIL_FROM, emails)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
    return 0


def send_email_to_me(title, content, type='text', async=True):
    from django.conf import settings
    from www.tasks import async_send_email

    if async:
        async_send_email.delay(settings.MY_EMAIL, title, content)
    else:
        async_send_email(settings.MY_EMAIL, title, content)


def get_clientip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        arr_ip = client_ip.split(',', 1)
        return arr_ip[0].strip()
    elif 'HTTP_X_REAL_IP' in request.META:
        return request.META['HTTP_X_REAL_IP']
    else:
        return request.META.get('REMOTE_ADDR', u'127.0.0.1')


def time_format(value):
    import time
    import datetime

    if not value:
        return 'datetime error'
    d = value
    if not isinstance(value, datetime.datetime):
        d = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    now_date = datetime.datetime.now()
    ds = time.time() - time.mktime(d.timetuple())  # 秒数
    # dd = now_date - d  # 日期相减对象
    if ds <= 5:
        return u'刚刚'
    if ds < 60:
        return u'%d秒前' % ds
    if ds < 3600:
        return u'%d分钟前' % (ds / 60,)
    d_change = now_date.day - d.day
    if ds < 3600 * 24 * 3:
        if d_change == 0:
            return u'今天%s' % d.strftime('%H:%M:%S')
        if d_change == 1:
            return u'昨天%s' % d.strftime('%H:%M:%S')
        if d_change == 2:
            return u'前天%s' % d.strftime('%H:%M:%S')
    y_change = now_date.year - d.year
    if y_change == 0:
        return u'%s' % d.strftime('%m-%d %H:%M:%S')
    if y_change == 1:
        return u'去年%s' % d.strftime('%m-%d %H:%M:%S')
    return u'%s年前%s' % (y_change, unicode(d.strftime('%m月%d日'), 'utf8'))


def escape_text(str):
    newStr = str or ''
    newStr = newStr.strip()
    # 注意替换的值是有严格顺序的
    newStr = str.replace('&', '&amp;') \
        .replace(' ', '&nbsp;') \
        .replace('>', '&gt;') \
        .replace('<', '&lt;') \
        .replace('\n', '&nbsp;&nbsp;&nbsp;')
    return newStr


def vlen(s, min_l, max_l):
    if min_l <= len(s) <= max_l:
        return True


def vemail(email):
    regexStr = ur"^[-_\w\.]+@([_\w]+\.)+[\w]{2,32}$"
    if not re.match(regexStr, email):
        return False
    return True


def vcontent(content):
    bads = (u'呵呵', u'哈哈', u'嘿嘿', u'测试', u'试下', u'test')
    if len(content) < 2 or content in bads:
        return
    return True


def get_function_code(func):
    return '%s_%s' % (func.__name__, func.func_code.co_filename.split('simplejoy')[-1].replace('/', '_').replace('\\', '_'))


if __name__ == '__main__':
    print vemail('lantian-_1212lz@163.com')
