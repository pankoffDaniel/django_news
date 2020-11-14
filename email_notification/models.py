from django.db import models
from django.utils.translation import ugettext_lazy as _


class EmailSubscriptionModel(models.Model):
    """Subscribed email to new posts."""
    email = models.EmailField('Email', unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Email subscription')
        verbose_name_plural = _('Email subscriptions')


class MailUsModel(models.Model):
    """Site Mail Us contact form."""
    email = models.EmailField('Email')
    question_subject = models.CharField(_('Mail subject'), max_length=255)
    question_message = models.TextField(_('Mail message'))
    answer_subject = models.CharField(_('Answer mail subject'), blank=True, max_length=255)
    answer_message = models.TextField(_('Answer mail message'), blank=True)
    answer_staff = models.CharField(_('Answer staff'), max_length=150, blank=True)
    is_answered = models.BooleanField(_('Is answered'), default=False, blank=True)

    def __str__(self):
        return self.question_subject

    class Meta:
        verbose_name = _('Mail letter')
        verbose_name_plural = _('Mail letters')
        ordering = ['-id']
