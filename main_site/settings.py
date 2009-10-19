from saaskit.settings import *

import os.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
APP_MEDIA_ROOT = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

SERVE_MEDIA = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rndx7w-jze@1$fu!&7x*b*mm&c!)!$5-@gvw^5^u_ixohmiipi'

ROOT_URLCONF = 'main_site.urls'

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.admindocs',
    )

try:
    from settings_local import *
except ImportError:
    pass
