# -*- coding: utf-8 -*-

import sys
import os
sys.path += ['/var/www', '/var/www/simplejoy']
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
