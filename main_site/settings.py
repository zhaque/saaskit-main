from saaskit.settings import *

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rndx7w-jze@1$fu!&7x*b*mm&c!)!$5-@gvw^5^u_ixohmiipi'

ROOT_URLCONF = 'main_site.urls'

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.admindocs',
)
                