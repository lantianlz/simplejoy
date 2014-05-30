# -*- coding: utf-8 -*-

from celery.task import task


@task(queue='blog_worker', name='blog_worker.email_send')
def async_send_email(emails, title, content, type='text'):
    from www.lib import utils
    return utils.send_email(emails, title, content, type='text')
