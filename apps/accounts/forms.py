# -*- coding: utf-8 -*-
import hashlib, time
import random
from datetime import datetime, timedelta

from django import forms
from django.conf import settings
from django.core import validators
from django.utils.safestring import mark_safe
from autoslug.settings import slugify
from autoslug.utils import generate_unique_slug

from activebuys.apps.utils.forms import EmErrorList
from activebuys.apps.accounts.models import Account, RestorePasswordRequest
from activebuys.apps.accounts.mails import send_confirm_email
from activebuys.apps.accounts.widgets import MyCheckboxSelectMultiple

class AdminAccountCreateForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(AdminAccountCreateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        """ Make sure an account with the same email address doesn't exist.
        Check for case-insensitive matches, since Foxycart assumes two emails 
        which match case-insensitive are the same. """
        email = self.cleaned_data["email"]
        try:
            Account.objects.get(email__iexact=email) # email__iexact, to catch case-insensitive matches
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super(AdminAccountCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminAccountChangeForm(forms.ModelForm):

    class Meta:
        model = Account

    def __init__(self, *args, **kwargs):
        super(AdminAccountChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email already exists.")


class RegistrationForm(AdminAccountCreateForm):
    """ This is the form with which a user will create their own account.

    Notable functionality:
     - saves a unique username based on the first 30 chars of the email address
     - verifies the password (enter twice, must match)
     - verifies that they've agreed to the terms (is_agree=True)
     - uses honeypot field to smoke out spambots
     - ensures that the form's life is not to short (to smoke out bots) or long
     - accepts a full name, and splits it into first and last names
     - creates a confirmation code for the user to find in their email inbox
     - ensures the user is not `active` until they use that confirm link

    """

    name = forms.CharField(
                widget=forms.TextInput(
                    attrs={'class':'blink','title':'Name'}
                ),
                initial="Name"
    )
    email = forms.EmailField(
                widget=forms.TextInput(
                    attrs={"class":"blink", "title":"Email Address"}
                ),
                initial="Email Address"
    )
    password1 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':"true-pass"}),
                initial=""
    )
    password2 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':"true-pass"}),
                initial=""
    )
    referred_email = forms.CharField(
                widget=forms.TextInput(
                    attrs={"class":"blink", "title":u"Friend’s Email / Org. Name"}
                ),
                initial=u"Friend’s Email / Org. Name"
    )
    is_agree = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'check'}))

    # fields for antispam
    timestamp = forms.IntegerField(widget=forms.HiddenInput)
    honeypot = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'style':'display:none;'}),
                               label='')

    class Meta:
        model = Account
        fields = ('name', 'email', 'password1', 'password2', 'subscribe_location', 'referred_email', 'is_agree')
        widgets = {
            'subscribe_location': MyCheckboxSelectMultiple(attrs={"class":"check"})
        }

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=EmErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(RegistrationForm, self).__init__(data, files, auto_id, prefix,
                 initial, error_class, label_suffix,
                 empty_permitted, instance)
                 
    def security_errors(self):
        """Return just those errors associated with security"""
        errors = ErrorDict()
        for f in ["honeypot", "timestamp"]:
            if f in self.errors:
                errors[f] = self.errors[f]
        return errors

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (> 2 hours) in the past or too close (< 9 sec)."""
        ts = self.cleaned_data["timestamp"]
        difference = time.time() - ts
        if difference > (2 * 60 * 60) or difference < 9:
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'timestamp'     : str(timestamp),
        }
        return security_dict

    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or name == 'Name':
            raise forms.ValidationError('This field is required') 
        return name

    def clean_referred_email(self):
        referred_email = self.cleaned_data.get('referred_email')
        if referred_email and\
              self.fields['referred_email'].initial == referred_email:
            return None
        return referred_email

    def generate_unique_username(self, username):
        """ Based on the email address, create a unique username in less than 
        30 chars. Example: email address is `somelongemailaddress@example.com`.
         - first, see if `somelongemailaddress@example.c` is available
         - next, see if `somelongemailaddress@example.#` is available for 0-9
         - next, see if `somelongemailaddress@example##` is available for 10-99
         - next, see if `somelongemailaddress@exampl###` is available for 100-999
         - etc.
         """
        orig_username = username[:30]
        index = 0
        while True:
            try:
                Account.objects.get(username=orig_username)
                index += 1
                orig_username = orig_username[:-len(str(index))] + str(index)
            except Account.DoesNotExist:
                return orig_username
 

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['name'].split(' ')[0]
        user.last_name = ' '.join(self.cleaned_data['name'].split(' ')[1:])
        user.username = self.generate_unique_username(self.cleaned_data['email'])
        # generate code for confirmation email
        user.confirm_email_code = generate_code(user)
        # make user inactive
        user.is_active = False
        user.save()
        # send confirmation mail
        send_confirm_email(user)
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
                widget=forms.TextInput(
                    attrs={"class":"blink", "title":"Email Address"}
                ),
                initial="Email Address",
                required=False
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"true-pass"}), required=False)
    def __init__(self, *args, **kwargs):
        self.user_cache = None
        kwargs['error_class'] = EmErrorList
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        from django.contrib.auth import authenticate

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(username=email, password=password) # 
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a valid email address and password. Note that the password is case sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        else:
            raise forms.ValidationError("Please enter a valid email address and password. Note that the password is case sensitive.")

    def get_user(self):
        return self.user_cache


class RestorePasswordForm(forms.Form):
    code = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':"true-pass"}),
                initial=""
    )
    password2 = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':"true-pass"}),
                initial=""
    )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=EmErrorList, label_suffix=':',
                 empty_permitted=False):
        self.cached_user = None
        super(RestorePasswordForm, self).__init__(data, files, auto_id, prefix,
                 initial, error_class, label_suffix,
                 empty_permitted)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Password fields didn't match.")
        return password2

    def clean_code(self):
        # if code older then 3 days, user must take one more
        try:
            req = RestorePasswordRequest.objects.get(
                code=self.cleaned_data['code'],
                timestamp__gte=datetime.now()-timedelta(days=3)
            )
            self.cached_user = req.account
        except RestorePasswordRequest.DoesNotExist:
            raise forms.ValidationError('Code is out of date')
        return self.cleaned_data['code']

    def change_password(self):
        self.cached_user.set_password(self.cleaned_data['password1'])
        self.cached_user.save()


def build_change_form(fields):
    fields.remove('csrfmiddlewaretoken')
    fs = fields
    class FormClass(forms.ModelForm):
        if 'password1' in fs:
            password1 = forms.CharField(widget=forms.PasswordInput)
        if 'password2' in fs:
            password2 = forms.CharField(widget=forms.PasswordInput)
        if 'first_name' in fs:
            first_name = forms.CharField()
        if 'last_name' in fs:
            last_name = forms.CharField()

        class Meta:
            model = Account
            fields = fs

        def __init__(self, *args, **kwargs):
            super(FormClass, self).__init__(*args, **kwargs)

        def clean_password2(self):
            password1 = self.cleaned_data.get("password1", "")
            password2 = self.cleaned_data["password2"]
            if password1 != password2:
                raise forms.ValidationError("Password fields didn't match.")
            return password2

        def clean_email(self):
            email = self.cleaned_data["email"]
            try:
                if not self.instance:
                    Account.objects.get(email=email)
                else:
                    Account.objects.get(email=email, id=self.instance.id)
                    return email
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("A user with that email already exists.")

        def save(self, commit=True):
            inst = super(FormClass, self).save(commit=False)
            if self.cleaned_data.get('password1'):
                inst.set_password(self.cleaned_data.get('password1'))
            if commit:
                inst.save()
            return inst

    return FormClass

def generate_code(user):
    """ Generate and return account activation code """
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    return hashlib.sha224(settings.SECRET_KEY+salt+user.email+user.username).hexdigest()

