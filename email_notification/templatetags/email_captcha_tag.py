from django import template

from email_notification.forms import EmailSubscriptionForm


register = template.Library()


@register.simple_tag
def get_email_subscription_captcha_form():
    """Captcha form."""
    return EmailSubscriptionForm()
