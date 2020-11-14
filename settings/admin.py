from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from src import utils

from .models import SiteSocialNetModel, SiteMainSettingsModel, SiteContactsModel


@admin.register(SiteContactsModel)
class SiteContactsAdmin(admin.ModelAdmin):
    """Admin form of site contacts."""
    list_display = ('id', 'phone_number', 'email', 'address')
    list_display_links = ('id', 'phone_number', 'email', 'address')

    def has_add_permission(self, request):
        """If there are 1 row, then hide the adding button"""
        return SiteContactsModel.objects.count() < 1


@admin.register(SiteSocialNetModel)
class SiteSocialNetAdmin(admin.ModelAdmin):
    """Admin form of site social net."""
    list_display = ('id', 'title', 'url', 'get_image')
    list_display_links = ('id', 'title')
    fields = ('title', 'url', 'image', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return utils.get_image(obj.image, width=100, alt=_('Image'))

    get_image.short_description = _('Image')


@admin.register(SiteMainSettingsModel)
class SiteSettingsAdmin(TranslationAdmin):
    """Admin form of site settings."""
    list_display = ('id', 'title', 'description', 'get_logo_1_image', 'get_logo_2_image',
                    'get_default_user_avatar', 'get_default_guest_avatar', 'get_deleted_avatar')
    list_display_links = ('id', 'title')
    fields = (
        'title', 'description',
        ('logo_1_image', 'get_logo_1_image'),
        ('logo_2_image', 'get_logo_2_image'),
        ('user_avatar', 'get_default_user_avatar'),
        ('guest_avatar', 'get_default_guest_avatar'),
        ('deleted_avatar', 'get_deleted_avatar'),
    )
    readonly_fields = ('get_logo_1_image', 'get_logo_2_image',
                       'get_default_user_avatar', 'get_default_guest_avatar', 'get_deleted_avatar')

    def has_add_permission(self, request):
        """If there are 1 row, then hides the adding button"""
        return SiteMainSettingsModel.objects.count() < 1

    def get_logo_1_image(self, obj):
        return utils.get_image(obj.logo_1_image, width=100, alt=_('Main logo'))

    def get_logo_2_image(self, obj):
        return utils.get_image(obj.logo_2_image, width=100, alt=_('Alternative logo'))

    def get_default_user_avatar(self, obj):
        return utils.get_image(obj.user_avatar, width=100, alt=_('User avatar'))

    def get_default_guest_avatar(self, obj):
        return utils.get_image(obj.guest_avatar, width=100, alt=_('Guest avatar'))

    def get_deleted_avatar(self, obj):
        return utils.get_image(obj.deleted_avatar, width=100, alt=_('Deleted avatar'))

    get_logo_1_image.short_description = _('Logo')
    get_logo_2_image.short_description = _('Alternative logo')
    get_default_user_avatar.short_description = _('User avatar')
    get_default_guest_avatar.short_description = _('Guest avatar')
    get_deleted_avatar.short_description = _('Deleted avatar')
