from django import forms
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import PostCommentModel


class PostCommentForm(forms.ModelForm):
    """Post comment of form."""
    captcha = ReCaptchaField()

    class Meta:
        model = PostCommentModel
        widgets = {
            'email': forms.EmailInput(attrs={"class": "input", "placeholder": "Email"}),
            'name': forms.TextInput(attrs={"class": "input", "placeholder": pgettext_lazy('Contact form', "Name")}),
            'message': forms.Textarea(attrs={"id": "comment", "class": "input", "placeholder": _("Message")})
        }
        fields = ('email', 'name', 'message', 'captcha')
