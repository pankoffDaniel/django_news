from django.urls import path

from comments.views import add_comment, action_comment


urlpatterns = [
    path('add/', add_comment, name='add_comment'),
    path('action/', action_comment, name='action_comment'),
]
