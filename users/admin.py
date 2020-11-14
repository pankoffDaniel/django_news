from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from src import utils
from .models import UserModel


@admin.register(UserModel)
class CustomUserAdmin(UserAdmin, admin.ModelAdmin):
    """Admin form of custom user."""
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'get_user_avatar')
    list_display_links = ('id', 'first_name', 'last_name', 'username')
    readonly_fields = ('get_user_avatar',)
    ordering = ('date_joined',)
    fieldsets = (
        (_('Authentication'), {
            'fields': (
                'email', 'password'
            )
        }),
        (_('Personal info'), {
            'fields': (
                ('avatar', 'get_user_avatar'), 'username', 'first_name', 'last_name', 'about'
            )
        }),
        (_('Social nets'), {
            'fields': (
                'social_facebook', 'social_twitter', 'social_google', 'social_instagram'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login', 'date_joined'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2'
            ),
        }),
    )

    save_on_top = True

    def get_user_avatar(self, obj):
        return utils.get_image(obj.avatar, width=100, alt=_('User avatar'))

    get_user_avatar.short_description = _('Avatar')
