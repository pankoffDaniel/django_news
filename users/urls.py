from django.urls import path

from users.views import user_login, user_logout, user_register, confirm_user_register, \
    user_restore, confirm_user_restore, create_new_user_password


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/submit/', confirm_user_register, name='confirm_register'),
    path('register/', user_register, name='register'),
    path('restore/new-password/', create_new_user_password, name='create_new_password'),
    path('restore/submit/', confirm_user_restore, name='confirm_restore'),
    path('restore/', user_restore, name='restore'),
]
