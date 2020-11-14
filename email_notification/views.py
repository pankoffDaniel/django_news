from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from email_notification import services
from email_notification.forms import EmailSubscriptionForm, MailUsForm
from email_notification.tasks import send_mail_function


def subscribe_email(request):
    """Subscribes got email for new posts."""
    if request.method != 'POST':
        raise PermissionDenied()
    form = EmailSubscriptionForm(request.POST)
    if form.is_valid():
        subject = 'Pankoff Industries'
        message = 'You have been subscribed successfully!.\nYou will get only new posts!'
        send_from = settings.EMAIL_HOST_USER
        email_list = [form.cleaned_data['email']]
        send_mail_function.delay(subject, message, send_from, email_list, countdown=5 * 60, max_retries=3)
        messages.success(request, _('You have been subscribed successfully!'))
        form.save()
    else:
        if services.check_email_exists_in_email_subscriptions(request.POST.get('email')):
            messages.warning(request, _('Email is already subscribed!'))
        else:
            messages.error(request, _('Please check Email correct or try later'))
    return redirect(request.META.get('HTTP_REFERER'))


def mail_us(request):
    """Sends a user letter to the admin panel."""
    if request.method != 'POST':
        raise PermissionDenied()
    form = MailUsForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, _('Your mail was delivered!'))
    else:
        messages.error(request, _('Please check Email correct or try later'))
    return redirect(request.META.get('HTTP_REFERER'))
