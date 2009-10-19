### -*- coding: utf-8 -*- ####################################################

from settings import *

DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False

EMAIL_DEBUG = DEBUG

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

SERVE_MEDIA = False
