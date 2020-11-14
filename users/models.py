from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from settings.models import SiteMainSettingsModel


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractUser):
    """Additional fields of user model."""
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=30)
    email = models.EmailField('Email', unique=True)
    avatar = models.ImageField(_('Avatar'), upload_to='images/users', blank=True)
    about = models.TextField(_('About'), blank=True)
    social_facebook = models.URLField('Facebook', blank=True)
    social_twitter = models.URLField('Twitter', blank=True)
    social_google = models.URLField('Google', blank=True)
    social_instagram = models.URLField('Instagram', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('author', kwargs={'slug': self.username})

    def save(self, *args, **kwargs):
        # If there is main settings then "avatar" field equals
        # "user_avatar" field from settings, else - text "No image"
        if not self.avatar:
            try:
                self.avatar = SiteMainSettingsModel.objects.first().user_avatar
            except AttributeError:
                self.avatar = 'No image'
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
