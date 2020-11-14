from django import template

from users.forms import UserLoginForm


register = template.Library()


@register.simple_tag
def get_user_captcha_form():
    """Captcha form."""
    return UserLoginForm()
