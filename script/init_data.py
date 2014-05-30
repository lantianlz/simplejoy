# -*- coding: utf-8 -*-

import sys
import os
sys.path.extend(['E:\\workspace\\google_code\\simplejoy', 'E:\\workspace\\google_code\\simplejoy\\www'])
sys.path.extend(['/var/www/simplejoy', '/var/www/simplejoy/www'])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

from www.blog.models import Category


def init_category():
    data = (
        (u'闲言碎语', u'', u'xysy', 100, True),
        (u'吃货日记', u'', u'chrj', 6, False),
        (u'天马行空', u'', u'tmxk', 5, True),
        (u'若有所思', u'人类一思考，上帝就发笑', u'ryss', 4, True),
        (u'沧海一粟', u'一粟、二粟、三粟......方成沧海', u'chys', 2, True),
        (u'它山之石', u'可以攻玉', u'tszs', 3, False),
        (u'程序人生', u'', u'cxrs', 1, True),
    )

    for d in data:
        name, title, domain, sort_num, state = d

        ps = dict(name=name, title=title, domain=domain, sort_num=sort_num, state=state)
        c = Category.objects.create(**ps)
        if not domain:
            c.domain = c.id
            c.save()


def main():
    init_category()


if __name__ == '__main__':
    main()
