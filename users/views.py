import random
import time

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from email_notification.tasks import send_mail_function
from users.forms import UserLoginForm, UserRegisterForm, UserSubmitActionForm, UserRestoreForm, UserNewPasswordForm
from .models import UserModel


def user_login(request):
    """Authenticates user and redirecting him on main page."""
    if request.user.is_authenticated:
        return redirect('home')
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """Closes user session and redirecting him on login page."""
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def user_register(request):
    """Creates confirmation code and redirects to confirm user registration if form is valid."""
    if request.user.is_authenticated:
        return redirect('home')
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['username'] = form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password1']
            send_confirmation_code(request, 'Continue your registration')
            return redirect('confirm_register')
    return render(request, 'users/register.html', {'form': form})


def confirm_user_register(request):
    """If validation codes are matches in form then registers new user and redirects on home page."""
    form = UserSubmitActionForm()
    if request.method == 'POST':
        if request.POST.get('resend'):
            if time.time() - request.session.get('timeout', 0) < 60:
                time_left = 60 - int(time.time() - request.session.get('timeout', 0))
                messages.warning(request, _(f'Wait for {time_left} seconds'))
            else:
                request.session['timeout'] = time.time()
                messages.success(request, _('Check your email'))
                send_confirmation_code(request, 'Continue your registration')
        else:
            form = UserSubmitActionForm(request.POST, confirmation_code=request.session.get('confirmation_code'))
            if form.is_valid():
                first_name = request.session.get('first_name')
                last_name = request.session.get('last_name')
                username = request.session.get('username')
                email = request.session.get('email')
                password = request.session.get('password')

                user = UserModel.objects.create(first_name=first_name, last_name=last_name,
                                                username=username, email=email)
                user.set_password(password)
                user.save()
                login(request, user)

                subject = 'You have been registered on Callie!'
                message = f'Visit us on link:\n' \
                          f'{settings.DOMAIN_URL}'
                send_from = settings.EMAIL_HOST_USER
                email_list = [email]
                send_mail_function.delay(subject, message, send_from, email_list, countdown=60 * 5, max_retries=3)
                messages.success(request, _('You have been registered successfully!'))
                return redirect('home')
    return render(request, 'users/confirm_register.html', {'form': form})


def user_restore(request):
    """Creates confirmation code and redirects to confirm user password restoring if form is valid."""
    form = UserRestoreForm()
    if request.method == 'POST':
        form = UserRestoreForm(request.POST)
        if form.is_valid():
            if UserModel.objects.filter(email=form.cleaned_data['email']).exists():
                request.session['email'] = form.cleaned_data['email']
                send_confirmation_code(request, 'Restoring account password!')
                return redirect('confirm_restore')
    return render(request, 'users/restore_password.html', {'form': form})


def confirm_user_restore(request):
    """If validation codes are matches in form then redirects to create new password."""
    form = UserSubmitActionForm()
    if request.method == 'POST':
        if request.POST.get('resend'):
            if time.time() - request.session.get('timeout', 0) < 60:
                time_left = 60 - int(time.time() - request.session.get('timeout', 0))
                messages.warning(request, _(f'Wait for {time_left} seconds'))
            else:
                request.session['timeout'] = time.time()
                messages.success(request, _('Check your email'))
                send_confirmation_code(request, _('Restoring account password!'))
        else:
            form = UserSubmitActionForm(request.POST, confirmation_code=request.session.get('confirmation_code'))
            if form.is_valid():
                return redirect('create_new_password')
    return render(request, 'users/confirm_restore.html', {'form': form})


def create_new_user_password(request):
    """Creates news user password."""
    form = UserNewPasswordForm()
    if request.method == 'POST':
        form = UserNewPasswordForm(request.POST)
        if form.is_valid():
            email = request.session.get('email')
            new_password = form.cleaned_data['password2']
            user = UserModel.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, _('Password was changed successfully!'))
            subject = 'Your password was changed!'
            message = 'If you didn\'t do this action change your password!'
            send_from = settings.EMAIL_HOST_USER
            email_list = [email]
            send_mail_function.delay(subject, message, send_from, email_list, countdown=60 * 5, max_retries=3)
            return redirect('login')
    return render(request, 'users/create_new_password.html', {'form': form})


def send_confirmation_code(request, subject):
    """Generates new confirmation code and send in on written email."""
    confirmation_code = str(random.randint(1000, 9999))
    request.session['confirmation_code'] = confirmation_code

    message = f'Confirmation code: {confirmation_code}'
    send_from = settings.EMAIL_HOST_USER
    email_list = [request.session.get('email')]
    send_mail_function.delay(subject, message, send_from, email_list, countdown=60 * 5, max_retries=3)
