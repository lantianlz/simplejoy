# -*- coding: utf-8 -*-
# Django settings for www project.


import os
DEBUG = False
TEMPLATE_DEBUG = DEBUG
LOCAL_FLAG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

EMAIL_FROM = u'"简单的快乐的博客" <blog@simplejoy.me>'
EMAIL_HOST_USER = 'blog@simplejoy.me'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = '25'
MY_EMAIL = 'lantian-lz@163.com'

MEDIA_VERSION = '000'

SERVER_NAME = 'DEVELOP' if LOCAL_FLAG else 'BLOG_WEB0'

if not LOCAL_FLAG:
    SITE_DOMAIN = u'simplejoy.me'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '/var/www/simplejoy/blog_db',  # Or path to database file if using sqlite3.
            'USER': '',  # Not used with sqlite3.
            'PASSWORD': '',  # Not used with sqlite3.
            'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        },
    }
else:
    SITE_DOMAIN = u'a.com'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'blog',  # Or path to database file if using sqlite3.
            'USER': 'root',  # Not used with sqlite3.
            'PASSWORD': '851129',  # Not used with sqlite3.
            'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',  # Set to empty string for default. Not used with sqlite3.
        },
    }

# DATABASE_ROUTERS = ['useraccount.router.UseraccountRouter', 'comment.router.CommentRouter', 'club.router.ClubRouter',
#                    'privatemsg.router.PrivateMSGRouter', 'group.router.GroupRouter', ]

TIME_ZONE = 'Asia/Shanghai'
DATETIME_FORMAT = 'Y-m-d H:i'
DATE_FORMAT = 'Y-m-d'

LANGUAGE_CODE = 'zh-cn'  # 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

# 引入父目录来引入其他模块
import sys
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../'))])


MEDIA_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../media'))
MEDIA_URL = 'http://static.%s/' % SITE_DOMAIN

STATIC_ROOT = os.path.abspath(os.path.join(SITE_ROOT, '../static_root_s'))
STATIC_URL = '/static/'
STATIC_URL = 'http://static.%s/' % SITE_DOMAIN
ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '$o8f##ie)5oroy&s@$h9)lxk1a)2uoh2x$kcbu*05nbhr%n-9q'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'www.middleware.ErrorInfoMidware',
)

ROOT_URLCONF = 'www.urls'
TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(SITE_ROOT, 'templates')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",

    "www.lib.context_processors.config",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',

    'www.custom_tags',
    'www.blog',
    'www.comment',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


SESSION_COOKIE_HTTPONLY = True  # 能防止xss漏洞
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 12               # Age of cookie, in seconds (default: 2 weeks).

import logging
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s ---------- %(pathname)s:%(module)s.%(funcName)s Line:%(lineno)d',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)
