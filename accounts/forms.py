from datetime import timedelta

from django import forms

from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _




class UserCacheMixin:
    user_cache = None


class SignIn(UserCacheMixin, forms.Form):
    password = forms.CharField(label=_(''), strip=False,
                               widget=forms.PasswordInput(attrs={'placeholder': "password"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if settings.USE_REMEMBER_ME:
            self.fields['remember_me'] = forms.BooleanField(label=_('Remember me'), required=False)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user_cache:
            return password

        if not self.user_cache.check_password(password):
            raise ValidationError(_('You entered an invalid password.'))

        return password


class SignInViaUsernameForm(SignIn):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'placeholder': "Username"}))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['username', 'password', 'remember_me']
        return ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError(_('You entered an invalid username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return username


class SignInViaEmailForm(SignIn):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email', 'password', 'remember_me']
        return ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email


class SignInViaEmailOrUsernameForm(SignIn):
    email_or_username = forms.CharField(label=_(''), widget=forms.TextInput(attrs={'placeholder': "Email or Username"}))

    @property
    def field_order(self):
        if settings.USE_REMEMBER_ME:
            return ['email_or_username', 'password', 'remember_me']
        return ['email_or_username', 'password']

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email_or_username


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = settings.SIGN_UP_FIELDS

    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))
    username = forms.CharField(label=_(''),
                               widget=forms.TextInput(attrs={'placeholder': "Username"}))
    password1 = forms.CharField(label=_(""),
                                strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'new-password', 'placeholder': 'Password'}, ),
                                )
    password2 = forms.CharField(label=_(""),
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm'}),
                                strip=False,
                                )



class ResendActivationCodeForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_(""),
                                        widget=forms.TextInput(attrs={'placeholder': "Email or username"}))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if user.is_active:
            raise ValidationError(_('This account has already been activated.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code not found.'))

        now_with_shift = timezone.now() - timedelta(hours=2)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Activation code has already been sent. You can request a new code in 2 hours.'))

        self.user_cache = user

        return email_or_username


class ResendActivationCodeViaEmailForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if user.is_active:
            raise ValidationError(_('This account has already been activated.'))

        activation = user.activation_set.first()
        if not activation:
            raise ValidationError(_('Activation code not found.'))

        now_with_shift = timezone.now() - timedelta(hours=2)
        if activation.created_at > now_with_shift:
            raise ValidationError(_('Activation code has already been sent. You can request a new code in 2 hours.'))

        self.user_cache = user

        return email


class RestorePasswordForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email


class RestorePasswordViaEmailOrUsernameForm(UserCacheMixin, forms.Form):
    email_or_username = forms.CharField(label=_(''), widget=forms.TextInput(attrs={'placeholder': "Username or email "
                                                                                                  "address"}))

    def clean_email_or_username(self):
        email_or_username = self.cleaned_data['email_or_username']

        user = User.objects.filter(Q(username=email_or_username) | Q(email__iexact=email_or_username)).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address or username.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email_or_username





class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']

        if email == self.user.email:
            raise ValidationError(_('Please enter another email.'))

        user = User.objects.filter(Q(email__iexact=email) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('You can not use this mail.'))

        return email


class ChangeUserNameForm(forms.Form):
    username = forms.CharField(label=_(''), widget=forms.TextInput(attrs={'placeholder': "User name"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        username = self.cleaned_data['username']

        if username == self.user.username:
            raise ValidationError(_('Please enter another username.'))

        user = User.objects.filter(Q(username__exact=username) & ~Q(id=self.user.id)).exists()
        if user:
            raise ValidationError(_('You can not use this username.'))

        return username


class RemindUsernameForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError(_('You entered an invalid email address.'))

        if not user.is_active:
            raise ValidationError(_('This account is not active.'))

        self.user_cache = user

        return email


def twitter_user():
    return True


class ChangeTwitterForm(forms.Form):
    positive_words = forms.CharField(label=_(''), widget=forms.Textarea(attrs={f'placeholder': f'Write the positves '
                                                                                               f'words seperated by '
                                                                                               f'comma',
                                                                               'resize': 'none', 'rows': 5,
                                                                               'cols': 30}), required=False)

    negative_words = forms.CharField(label=_(''), widget=forms.Textarea(attrs={'placeholder': f'Write the negative '
                                                                                              f'words seperated by '
                                                                                              f'comma',
                                                                               'resize': 'none', 'rows': 5,
                                                                               'cols': 27}), required=False)

    email = forms.EmailField(label=_(''), widget=forms.EmailInput(attrs={'placeholder': "Email address"}))

    username = forms.CharField(label=_(''), widget=forms.TextInput(attrs={'placeholder': f'Username'}))
