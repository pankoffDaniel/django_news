from django import forms
from django.utils.translation import ugettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import EmailSubscriptionModel, MailUsModel


class EmailSubscriptionForm(forms.ModelForm):
    """Email subscription form."""
    captcha = ReCaptchaField()

    class Meta:
        model = EmailSubscriptionModel
        fields = '__all__'


class MailUsForm(forms.ModelForm):
    """Mail Us form."""
    captcha = ReCaptchaField()

    class Meta:
        model = MailUsModel
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    "class": "input",
                    "placeholder": "Email",
                }),
            'question_subject': forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": _("Subject"),
                    "autocomplete": "off",
                }),
            'question_message': forms.Textarea(
                attrs={
                    "class": "input",
                    "placeholder": _("Message"),
                    "autocomplete": "off",
                }),
        }


class MailUsAdminForm(forms.ModelForm):
    """Making fields answer_subject and answer_message required."""
    answer_subject = forms.CharField(label=_('Answer mail subject'), required=True)
    answer_message = forms.CharField(label=_('Answer mail message'), widget=forms.Textarea(), required=True)

    class Meta:
        model = MailUsModel
        fields = '__all__'
