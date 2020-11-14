from django.urls import path

from .views import subscribe_email, mail_us


urlpatterns = [
    path('post_subscribe/', subscribe_email, name='post_subscribe'),
    path('mail_us/', mail_us, name='mail_us'),
]
