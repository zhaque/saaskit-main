
import random, string

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from registration.models import RegistrationProfile
from django_authopenid.forms import attrs_dict

# favour django-mailer but fall back to django.core.mail
if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    first_name = forms.CharField(_('first name'), required=False)
    last_name = forms.CharField(_('last name'), required=False)
    
    redirect_to = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']
    
    @staticmethod
    def _gerenate_password(length=10):
        return ''.join([random.choice(string.digits+string.letters) 
                        for i in range(length)])
    
    def save(self):
        """
        Generate password.
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User`` (by calling
        ``RegistrationProfile.objects.create_inactive_user()``).

        """
        password = self._gerenate_password()
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=password,
                                                                    email=self.cleaned_data['email'],
                                                                    redirect_to=self.cleaned_data.get('redirect_to'))
        
        if 'first_name' in self.cleaned_data or 'last_name' in self.cleaned_data:
            new_user.first_name = self.cleaned_data.get('first_name')
            new_user.last_name = self.cleaned_data.get('last_name')
            new_user.save()
        
        current_site = Site.objects.get_current()
        subject = render_to_string('registration/credentials_subject.txt',
                                       { 'site': current_site })
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/credentials_email.txt',
                                   { 'username': self.cleaned_data['username'],
                                     'password': password,
                                     'site': current_site })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        
        return new_user
