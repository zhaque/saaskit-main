
import random, string

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from registration.models import RegistrationProfile
from django_authopenid.signals import oid_register
from django_authopenid.forms import attrs_dict

# favour django-mailer but fall back to django.core.mail
if 'mailer' in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail

class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    first_name = forms.CharField(_('first name'), required=False)
    last_name = forms.CharField(_('last name'), required=False)
    
    redirect_to = forms.CharField(widget=forms.HiddenInput, required=False)

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
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['email'],
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
                                   { 'email': new_user.email,
                                     'password': password,
                                     'site': current_site })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [new_user.email])
        
        return new_user


def register_account_email(form, _openid):
    """ create an account """
    user = User.objects.create_user(form.cleaned_data['email'], 
                            form.cleaned_data['email'])
    user.backend = "django.contrib.auth.backends.ModelBackend"
    oid_register.send(sender=user, openid=_openid)
    return user


class OpenidRegisterForm(forms.Form):
    """ openid signin form """
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, 
        maxlength=200)), label=u'Email address')
        
    def __init__(self, *args, **kwargs):
        super(OpenidRegisterForm, self).__init__(*args, **kwargs)
        self.user = None
    
    def clean_email(self):
        """For security reason one unique email in database"""
        if 'email' in self.cleaned_data:
            try:
                user = User.objects.get(email = self.cleaned_data['email'])
            except User.DoesNotExist:
                return self.cleaned_data['email']
            except User.MultipleObjectsReturned:
                raise forms.ValidationError(u'There is already more than one \
                    account registered with that e-mail address. Please try \
                    another.')
            raise forms.ValidationError(_("This email is already \
                registered in our database. Please choose another."))
                