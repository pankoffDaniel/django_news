from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from comments.models import PostCommentModel
from settings.models import SiteMainSettingsModel
from src import utils


@admin.register(PostCommentModel)
class PostCommentAdmin(admin.ModelAdmin):
    """Admin form of post comment."""
    list_display = ('id', 'comment_author', 'name', 'get_email', 'created_at', 'is_deleted')
    list_display_links = ('id', 'comment_author', 'name')
    fields = ('local_id', 'comment_author', 'get_email', 'message', 'post', 'parent', 'created_at', 'get_avatar',
              'is_deleted')
    readonly_fields = ('local_id', 'comment_author', 'name', 'get_email', 'message', 'post', 'parent', 'created_at',
                       'get_avatar')
    list_filter = ('is_deleted', 'created_at')
    list_editable = ('is_deleted',)

    def get_email(self, obj):
        if obj.comment_author:
            return obj.comment_author.email
        return obj.email

    def get_avatar(self, obj):
        if obj.comment_author:
            return utils.get_image(obj.comment_author.avatar, width=100, alt=_('User avatar'))
        return utils.get_image(SiteMainSettingsModel.objects.first().guest_avatar, width=100, alt=_('Guest avatar'))

    def has_add_permission(self, request):
        return False

    get_avatar.short_description = _('Avatar')
    get_email.short_description = _('Email')
