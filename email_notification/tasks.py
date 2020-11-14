from django.core.mail import send_mail
from django_news.celery import app


@app.task(bind=True)
def send_mail_function(self, subject, message, send_from, email_list, countdown, max_retries):
    """Sends async email."""
    try:
        send_mail(subject, message, send_from, email_list, fail_silently=True)
    except Exception as exc:
        self.retry(exc=exc, countdown=countdown, max_retries=max_retries)
