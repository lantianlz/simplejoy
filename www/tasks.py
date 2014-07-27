# -*- coding: utf-8 -*-

from celery.task import task
from www.lib import utils


@task(queue='blog_worker', name='blog_worker.email_send')
def async_send_email(emails, title, content, type='html'):
    return utils.send_email(emails, title, content, type=type)
