from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import UserModel


class UserLoginForm(forms.Form):
    """User login form."""
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Email",
                "type": "email",
            }))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": _("Password"),
            }))
    error_messages = {
        'invalid_login': _(
            "Enter a correct Email and password"
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
        )


class UserRegisterForm(UserCreationForm):
    """User register form."""
    captcha = ReCaptchaField()
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": "Email",
                "autocomplete": "off",
                "type": "email",
            }))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("First name"),
                "autocomplete": "on",
            }), max_length=30)
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("Last name"),
                "autocomplete": "on",
            }), max_length=30)
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("Username"),
                "autocomplete": "off",
            }))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": _("Password"),
                "autocomplete": "off",
            }), min_length=8)
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": _("Submit password"),
                "autocomplete": "off",
            }), min_length=8)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError(_('User with this Email already exists'))
        return email

    class Meta:
        model = UserModel
        fields = ('captcha', 'email', 'username', 'password1', 'password2')


class UserSubmitActionForm(forms.Form):
    captcha = ReCaptchaField()
    confirmation_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("Confirmation code"),
                "autocomplete": "off"
            }), required=False)

    def __init__(self, request=None, confirmation_code=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.confirmation_code = confirmation_code

    def clean_confirmation_code(self):
        input_confirmation_code = self.cleaned_data['confirmation_code']
        if input_confirmation_code == self.confirmation_code or self.confirmation_code is None:
            return input_confirmation_code
        raise ValidationError(_('Incorrect confirmation code!'))


class UserRestoreForm(forms.Form):
    captcha = ReCaptchaField()
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "input",
                "placeholder": _("Email"),
                "type": "email",
            }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            return email
        raise ValidationError(_('This Email is not registered!'))


class UserNewPasswordForm(forms.Form):
    captcha = ReCaptchaField()
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": _("Password"),
                "autocomplete": "off",
            }), min_length=8, required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input",
                "placeholder": _("Submit password"),
                "autocomplete": "off",
            }), min_length=8, required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password2 == password1:
            return password2
        raise ValidationError(_('The two password fields didn’t match'))
