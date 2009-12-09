### -*- coding: utf-8 -*- ####################################################

from copy import copy

from django.http import HttpResponseRedirect
from django.utils.http import urlquote_plus
from django.conf import settings 
from django.shortcuts import redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import apply_extra_context
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth.tokens import default_token_generator

from sso.views import sso
from django_authopenid.views import signin

from muaccounts.views.decorators import public
from muaccounts.utils import construct_main_site_url

from .forms import RegistrationForm 

def generic_signin(request, register_form=RegistrationForm, reg_success_url=None, register_action='register',
                   password_reset_form=PasswordResetForm, token_generator=default_token_generator, 
                   email_template_name='registration/password_reset_email.html',
                   password_reset_action='password_reset',
                   post_reset_redirect = 'django.contrib.auth.views.password_reset_done', 
                   redirect_field_name=REDIRECT_FIELD_NAME, 
                   extra_context=None, *args, **kwargs):
    
    if request.method == "POST" and password_reset_action in request.POST:
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            opts['domain_override'] = RequestSite(request).domain
            form.save(**opts)
            return redirect(post_reset_redirect)
        request.POST = {}
    else:
        form = password_reset_form()
    
    extra = {'password_reset_form': form, 'password_reset_action': password_reset_action}
    
    if request.method == 'POST' and register_action in request.POST:
        form = register_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reg_success_url or 'registration_complete')
        request.POST = {}
    else:
        initial = copy(request.GET)
        initial['redirect_to'] = request.GET.get(redirect_field_name, '')
        form = register_form(initial=initial)
    
    extra.update({'register_form': form, 'register_action': register_action})
    
    apply_extra_context(extra_context or {}, extra)
    
    return signin(request, extra_context=extra, *args, **kwargs)
