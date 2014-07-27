# -*- coding: utf-8 -*-

import datetime
from django.db import transaction
from django.conf import settings

from www.lib import cache, debug, utils
from www.comment.models import Comment, CommentCount
from www.tasks import async_send_email

# 需要国际化
dict_err = {
    001: u'和上句所说的话一样，稍显啰嗦',
    002: u'评论不存在或已经删除',
    003: u'权限不足',
    004: u'言之有物才可',
    005: u'评论对象不存在',
    006: u'更新评论对象评论数目出错',
    007: u'大名和邮箱必填',
    010: u'博客地址须已http://开头',
    011: u'唬我呢，什么邮箱格式!',
    012: u'请尽量让自己的回复有点意思',

    999: u'系统错误',
    000: u'成功',
}


class CommentOperateBase(object):

    def __init__(self):
        self.ccob = CommentCountOperateBase()

    def __del__(self):
        del self.ccob

    @transaction.commit_manually
    def add(self, nick, email, user_href, content, outerobj_type, outerobj, ip, create_time=None):
        """
        @attention: 添加评论
        """
        try:
            if not content:
                transaction.rollback()
                return False, dict_err.get(004)

            if not (nick and email):
                transaction.rollback()
                return False, dict_err.get(007)

            if user_href and not (user_href.startswith('http://') or user_href.startswith('https://')):
                transaction.rollback()
                return False, dict_err.get(010)

            if not utils.vemail(email):
                transaction.rollback()
                return False, dict_err.get(011)

            if not utils.vcontent(content):
                transaction.rollback()
                return False, dict_err.get(012)

            original_content = content
            # 转义特殊字符
            content = utils.escape_text(content)
            content = content[:512]

            cache_key = u'%s_%s' % ('pre_comment_', email)

            # 判断是否连续重复发送相同内容
            if cache.get(cache_key) == content:
                transaction.rollback()
                return False, dict_err.get(001)

            outerobj = self.get_outerobj(outerobj_type, outerobj) if isinstance(outerobj, (unicode, int)) else outerobj
            # 评论对象必须存在
            if not outerobj:
                transaction.rollback()
                return False, dict_err.get(005)

            ps = dict(email=email, nick=nick, user_href=user_href, content=content,
                      outerobj_type=self.get_outerobj_type_num(outerobj_type), ip=ip,
                      create_time=create_time or datetime.datetime.now())

            # 设置外部对象信息
            ps.setdefault('outerobj_id', outerobj.id)
            comment = Comment.objects.create(**ps)

            # 更新外部对象的冗余字段信息
            if not self.ccob.add_comment_count(outerobj_type, outerobj.id):
                transaction.rollback()
                return False, dict_err.get(006)

            # 缓存上一条发布的评论,ps:必须放到最后
            cache_key = u'%s_%s' % ('pre_comment_', email)
            cache.set(cache_key, content, time_out=600)

            context = dict(user_href=user_href, nick=nick, content=content, email=email, essay=outerobj)
            if email != settings.MY_EMAIL:
                e_content = utils.render_email_template('email/recevied_comment.html', context=context)
                utils.send_email_to_me(title=u'收到一条新的评论', content=e_content)

            # 通知at到的人
            at_nicks = select_at(content)
            for at_nick in at_nicks:
                at_email = get_user_email_by_nick(at_nick)
                if at_email and at_email != settings.MY_EMAIL and at_email != email:
                    e_content = utils.render_email_template('email/at.html', context=context)
                    async_send_email.delay(emails=at_email, title=u'收到一条来自simplejoy的博客的评论回复', content=e_content)

            transaction.commit()
            return True, comment
        except Exception, e:
            debug.log_debug_detail(e)
            transaction.rollback()
            return False, dict_err.get(999)

    @staticmethod
    def get_outerobj_title(outerobj_type, outerobj):
        """
        @attention: 获取外部对象对应的用户id
        """
        title = ''
        # 记录
        if outerobj_type == 'essay':
            title = outerobj.title
        return ('%s...' % title[:25]) if title.__len__() > 25 else title

    @staticmethod
    def get_outerobj(outerobj_type, outerobj_id):
        """
        @attention: 获取外部对象
        """
        outerobj = None

        from django.core.exceptions import ObjectDoesNotExist
        try:
            # 判断outerobj_type是否有效
            if CommentOperateBase.get_outerobj_type_num(outerobj_type) is None:
                return None

            # 记录
            elif outerobj_type == 'essay':
                from www.blog.models import Essay
                outerobj = Essay.objects.get(id=outerobj_id)
        except ObjectDoesNotExist:
            outerobj = None
        return outerobj

    def get_outerobj_comment(self, outerobj_type, outerobj_id):
        """
        @attention: 获取对象对应的评论
        """
        return Comment.objects.filter(
            outerobj_type=self.get_outerobj_type_num(
                outerobj_type),
            outerobj_id=outerobj_id).order_by('-id')

    @transaction.commit_manually
    def remove_comment(self, id, user):
        """
        @attention: 删除指定评论
        """
        try:
            try:
                comment = Comment.objects.get(id=id)
            except Comment.DoesNotExist:
                transaction.rollback()
                return False, dict_err.get(002)

            # 权限判断
            if not user.id:
                transaction.rollback()
                return False, dict_err.get(003)

            outerobj_type = comment.get_outerobj_type_display()
            # 更新外部对象的冗余字段信息
            outerobj = self.get_outerobj(outerobj_type, comment.outerobj_id)
            if outerobj:
                # 更新外部对象的冗余字段信息
                if not self.ccob.minus_comment_count(outerobj_type, comment.outerobj_id):
                    transaction.rollback()
                    return False, dict_err.get(006)
            else:
                pass

            comment.delete()
            transaction.commit()

            return True, dict_err.get(000)
        except Exception, e:
            transaction.rollback()
            debug.log_debug_detail(e)
            return False, dict_err.get(999)

    @staticmethod
    def get_outerobj_type_num(outerobj_type):
        """
        @attention: 获取外部类型code对应的整形表示
        """
        from www.comment.models import outerobj_type_choices
        for t in outerobj_type_choices:
            if str(t[1]) == str(outerobj_type):
                return t[0]
        return None


class CommentCountOperateBase(object):

    def add_comment_count(self, outerobj_type, outerobj_id, count=1):
        """
        @attention: 增加评论数
        """
        count = int(count)
        from django.db.models import F
        outerobj_type = CommentOperateBase(
        ).get_outerobj_type_num(outerobj_type)
        cc, created = CommentCount.objects.get_or_create(
            outerobj_type=outerobj_type, outerobj_id=outerobj_id,
            defaults=dict(update_time=datetime.datetime.now()))
        if created:
            cc.count += count
            cc.save()
        else:
            CommentCount.objects.filter(outerobj_type=outerobj_type, outerobj_id=outerobj_id)\
                .update(count=F('count') + count, update_time=datetime.datetime.now())

        # 清除缓存
        key = u'comment_count_cache_%s_%s' % (outerobj_type, outerobj_id)
        cache.delete(key)
        return True

    def minus_comment_count(self, outerobj_type, outerobj_id, count=1):
        count = int(count)
        from django.db.models import F
        outerobj_type = CommentOperateBase().get_outerobj_type_num(outerobj_type)
        CommentCount.objects.filter(outerobj_type=outerobj_type, outerobj_id=outerobj_id).update(count=F('count') - count)

        # 清除缓存
        key = u'comment_count_cache_%s_%s' % (outerobj_type, outerobj_id)
        cache.delete(key)
        return True

    def clear(self, outerobj_type, outerobj_id):
        """
        @attention: 清除对象
        """
        outerobj_type = CommentOperateBase().get_outerobj_type_num(outerobj_type)
        CommentCount.objects.filter(outerobj_type=outerobj_type, outerobj_id=outerobj_id).delete()

        # 清除缓存
        key = u'comment_count_cache_%s_%s' % (outerobj_type, outerobj_id)
        cache.delete(key)
        return True

    def get(self, outerobj_type, outerobj_id):
        """
        @attention: 获取数字信息
        """
        outerobj_type = CommentOperateBase(
        ).get_outerobj_type_num(outerobj_type)
        if outerobj_type is None:
            raise Exception, u'outerobj_type error'

        key = u'comment_count_cache_%s_%s' % (outerobj_type, outerobj_id)
        dict_cc = cache.get(key)
        if dict_cc is None:
            try:
                cc = CommentCount.objects.get(
                    outerobj_type=outerobj_type, outerobj_id=outerobj_id)
                dict_cc = dict(count=cc.count, update_time=cc.update_time)
            except CommentCount.DoesNotExist:
                dict_cc = dict(count=0, update_time=None)
            cache.set(key, dict_cc, time_out=3600 * 24)

        return dict_cc


def get_user_email_by_nick(nick):
    cs = list(Comment.objects.filter(nick=nick))
    if cs:
        return cs[0].email


def get_user_href_by_nick(nick):
    cs = list(Comment.objects.filter(nick=nick))
    user_href = ''
    if cs:
        user_href = cs[0].user_href
    return user_href or '###'


def select_at(s):
    """
    @attention: 寻找at对象名称
    """
    import re
    #@提到的用户名称必须是：中文，英文字符，数字，下划线，减号这四类
    p = re.compile(u'@([\w\-\u4e00-\u9fa5]+)', re.I)
    return list(set(p.findall(s)))  # 去掉重复提到的人


def replace_at_html(value):
    """
    @attention: 从内容中提取@信息
    """
    def _re_sub(match):
        """
        @attention: callback for re.sub
        """
        nick = match.group(1)
        # return '@<a href="/n/%(nick)s">%(nick)s</a>' % dict(nick=nick)
        return '@<a href="%(user_href)s" target="_blank">%(nick)s</a>' % dict(nick=nick, user_href=get_user_href_by_nick(nick))

    import re
    tup_re = (u'@([\w\-\u4e00-\u9fa5]+)', _re_sub)
    p = re.compile(tup_re[0], re.DOTALL | re.IGNORECASE)
    value = p.sub(tup_re[1], value)
    return value


def get_comment_page_onclick(page, outerobj_type, outerobj_id, comment_show_type, can_create_comment_permission):
    """
    @attention: 获取评论分页注册事件
    """
    return "get_comment('%s', '%s', '%s', '%s', '%s')" % (outerobj_type, outerobj_id, comment_show_type,
                                                          page, can_create_comment_permission)
