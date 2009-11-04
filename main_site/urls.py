from django.conf import settings
from django.conf.urls.defaults import *

handler404 = 'perfect404.views.page_not_found'

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', dict(template='about.html')),
    (r'^support/$', 'django.views.generic.simple.direct_to_template', dict(template='support.html')),
    (r'^privacy/$', 'django.views.generic.simple.direct_to_template', dict(template='tc.html')),
    url(r'^sso/$', 'sso.views.sso', name="sso"),
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^accounts/create-site/$', 'muaccounts.views.create_account'),
    (r'^profiles/', include('saaskit_profile.urls')),
    url(r'^subscription/(?P<object_id>\d+)/$', 'subscription.views.subscription_detail', 
     {'payment_method':'pro' if settings.PAYPAL_PRO else 'standard'}, name='subscription_detail'),
    (r'^subscription/', include('subscription.urls')),
    (r'^dashboard/', include('notification.urls')),
    (r'^contact/', include('contact_form.urls')),
    (r'^admin/templatesadmin/', include('templatesadmin.urls')),
    (r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# serve static files in debug mode
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
