from django.conf import settings

from email_notification.models import EmailSubscriptionModel
from .tasks import send_mail_function


def check_email_exists_in_email_subscriptions(email: str) -> bool:
    """Returns True if got email is already exists in list of email subscriptions."""
    return EmailSubscriptionModel.objects.filter(email=email).exists()


def notify_subscribers_new_post(post: object):
    """Notifies subscribers about new post."""
    subject = f'Author {post.author} published new post on the best site :)'
    post_url = post.get_absolute_url()
    content = f'{post.title}\n{settings.DOMAIN_URL}{post_url}'
    send_from = settings.EMAIL_HOST_USER
    email_list = list(EmailSubscriptionModel.objects.values_list('email', flat=True))
    send_mail_function.delay(subject, content, send_from, email_list, countdown=5 * 60, max_retries=3)
