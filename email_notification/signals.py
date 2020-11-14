from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_currentuser.middleware import get_current_authenticated_user

from email_notification.models import MailUsModel
from .tasks import send_mail_function


@receiver(post_save, sender=MailUsModel)
def email_notification(sender, instance, **kwargs):
    """
    Switches field is_published in True and send email notification
    after answer on guest question from contact form.
    """
    guest_email = instance.email
    guest_subject = instance.question_subject
    guest_message = instance.question_message
    send_from = settings.EMAIL_HOST_USER
    email_list = [guest_email]
    subject = instance.answer_subject

    if instance.is_answered:
        return

    if kwargs['created']:
        subject = 'We got your message!'
        message = f'---Your message---\n\n' \
                  f'Subject:\n{guest_subject}\n\n' \
                  f'Message:\n{guest_message}'
        send_mail_function.delay(subject, message, send_from, email_list, countdown=5 * 60, max_retries=3)

    elif not kwargs['created']:
        message = f'{instance.answer_message}\n\n' \
                  f'---Your message---\n\n' \
                  f'Subject:\n{guest_subject}\n\n' \
                  f'Message:\n{guest_message}\n\n' \
                  f'Best wishes, {get_current_authenticated_user().username}'
        send_mail_function.delay(subject, message, send_from, email_list, countdown=5 * 60, max_retries=3)

        instance.is_answered = True
        instance.answer_staff = get_current_authenticated_user().username
        instance.save()
