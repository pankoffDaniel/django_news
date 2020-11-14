from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class SiteSocialNetModel(models.Model):
    """Social Net of site."""
    title = models.CharField(_('Social net'), max_length=18, unique=True)
    url = models.URLField('URL')
    image = models.ImageField(_('Image'), upload_to='images/settings/social', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Social net')
        verbose_name_plural = _('Social nets')
        ordering = ['title']


class SiteMainSettingsModel(models.Model):
    """Main settings of site."""
    title = models.CharField(_('Site title'), max_length=18)
    description = models.TextField(_('Site description'))
    logo_1_image = models.ImageField(_('Site logo image'), upload_to='images/settings')
    logo_2_image = models.ImageField(_('Site alternative logo image'), upload_to='images/settings')
    user_avatar = models.ImageField(_('Default user avatar'), upload_to='images/settings')
    guest_avatar = models.ImageField(_('Default guest avatar'), upload_to='images/settings')
    deleted_avatar = models.ImageField(_('Deleted avatar'), upload_to='images/settings')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Main settings')
        verbose_name_plural = _('Main settings')


class SiteContactsModel(models.Model):
    """Settings of site contacts."""
    email = models.EmailField('Email')
    phone_number = models.CharField(_('Phone number'), max_length=18)
    address = models.CharField(_('Address'), max_length=255)

    def __str__(self):
        from django.utils.translation import ugettext as _
        return _('Contacts')

    @staticmethod
    def get_absolute_url():
        return reverse('contacts')

    class Meta:
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')
