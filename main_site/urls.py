from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from saaskit.urls import handler404, urlpatterns as saaskit_patterns

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', dict(template='about.html')),
    (r'^support/$', 'django.views.generic.simple.direct_to_template', dict(template='support.html')),
    (r'^privacy/$', 'django.views.generic.simple.direct_to_template', dict(template='tc.html')),
    (r'^accounts/create-site/$', 'muaccounts.views.create_account'),
    (r'^contact/', include('contact_form.urls')),
    (r'^admin/templatesadmin/', include('templatesadmin.urls')),
    (r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', include(admin.site.urls)),
)

#apply saaskit-core url mapping
urlpatterns += saaskit_patterns
