from django.apps import AppConfig


class EmailSendConfig(AppConfig):
    name = 'email_notification'
    verbose_name = 'Email'

    def ready(self):
        """Imports signals when app has been started"""
        import email_notification.signals
