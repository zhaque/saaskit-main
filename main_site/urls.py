from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from django.contrib import admin
admin.autodiscover()

from saaskit.urls import handler404, urlpatterns as saaskit_patterns, wrapped_queryset

from muaccounts.models import MUAccount
from muaccounts.forms import MUAccountForm

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', dict(template='index.html')),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', dict(template='about.html')),
    (r'^support/$', 'django.views.generic.simple.direct_to_template', dict(template='support.html')),
    (r'^privacy/$', 'django.views.generic.simple.direct_to_template', dict(template='tc.html')),
    (r'^contact/', include('contact_form.urls')),
    
    (r'^accounts/', include('django_authopenid.urls')),
    (r'^subscription/', include('subscription.urls')),
    (r'^profiles/', include('saaskit_profile.urls')),
    (r'^notices/', include('notification.urls')),
    
    (r'^admin/rosetta/', include('rosetta.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/templatesadmin/', include('templatesadmin.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    url(r'^muaccounts/$', 
        login_required(wrapped_queryset(object_list, lambda request, queryset: queryset.filter(owner=request.user))),
        {'template_object_name': 'mua', 'queryset': MUAccount.objects.all()}, 
        name='muaccounts_listing'),
    url(r'^content/add/(?P<app_label>muaccounts)/(?P<model_name>muaccount)/$', 
        'muaccounts.views.create_muaccount',
        {'form_exclude': ('about', 'logo', 'analytics_code', 'webmaster_tools_code', 'adsense_code', 
                          'yahoo_app_id', 'yahoo_secret', 'members'),
         'form_class': MUAccountForm,
         },
        name='frontendadmin_add'
    ),
    url(r'^content/change/(?P<app_label>muaccounts)/(?P<model_name>muaccount)/(?P<instance_id>[\d]+)/$', 
        'muaccounts.views.change_muaccount',
        {'form_exclude': ('owner', 'about', 'logo', 'analytics_code', 'webmaster_tools_code', 
                          'adsense_code', 'yahoo_app_id', 'yahoo_secret', 'members'),
         'form_class': MUAccountForm,
         },
        name='frontendadmin_change'
    ),
    url(r'^content/delete/(?P<app_label>muaccounts)/(?P<model_name>muaccount)/(?P<instance_id>[\d]+)/$',
        'muaccounts.views.delete_muaccount',
        name='frontendadmin_delete'
    ),
    
)

#apply saaskit-core url mapping
urlpatterns += saaskit_patterns
