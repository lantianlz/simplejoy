# -*- coding: utf-8 -*-

from www.comment import interface


def a():
    cob = interface.CommentOperateBase()

    outerobj_type = 'feed'
    outerobj_id = '162d81c0-3720-4b02-9d75-8b5526438861'
    objs = cob.get_outerobj_comment('match', '1')

#    print cob.clear_outerobj_comment(outerobj_type, outerobj_id)
    print cob.ccob.get(outerobj_type, outerobj_id)


if __name__ == '__main__':
    a()


# 1.装饰器的顺序
# 2.onering CS编程
# 3.django sentry 记录错误  onimaru
# 4.DAE SAE


# 周绮
# karais等异步MQ
