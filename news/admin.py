from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from src import utils
from .forms import PinnedPostForm, PostAdminForm
from .models import PostCategoryModel, PostTagModel, PostModel, PinnedPostModel, PostViewsModel


@admin.register(PostViewsModel)
class PostViewsAdmin(admin.ModelAdmin):
    """Admin form of post view."""
    list_display = ('id', 'post', 'ip', 'datetime')
    list_display_links = ('id', 'post')
    fields = ('post', 'ip', 'datetime')
    readonly_fields = ('post', 'ip', 'datetime')

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False


@admin.register(PostCategoryModel)
class PostCategoryAdmin(TranslationAdmin):
    """Admin form of post category."""
    list_display = ('id', 'title', 'get_image')
    list_display_links = ('id', 'title')
    fields = ('title', 'slug', 'image', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj: object) -> str:
        return utils.get_image(obj.image, width=100, alt=_('Category image'))

    get_image.short_description = _('Image')


@admin.register(PostTagModel)
class PostTagAdmin(TranslationAdmin):
    """Admin form of post tag."""
    list_display = ('id', 'title', 'get_image')
    list_display_links = ('id', 'title')
    fields = ('title', 'slug', 'image', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj: object) -> str:
        return utils.get_image(obj.image, width=100, alt=_('Tag image'))

    get_image.short_description = _('Image')


@admin.register(PinnedPostModel)
class PinnedPostAdmin(admin.ModelAdmin):
    """Admin form of pinned post."""
    form = PinnedPostForm
    list_display = ('id', 'pinned_post')
    list_display_links = ('id', 'pinned_post')

    def has_add_permission(self, request: object) -> bool:
        """If there are 3 pinned posts, then hides an adding button"""
        return PinnedPostModel.objects.count() < 3


@admin.register(PostModel)
class PostAdmin(TranslationAdmin):
    """Admin form of post."""
    form = PostAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'get_post_image', 'author', 'views',
                    'is_published', 'once_published')
    list_display_links = ('id', 'title')
    list_editable = ('is_published',)
    list_filter = ('category', 'tags', 'created_at')
    readonly_fields = ('author', 'views', 'get_header_image', 'get_post_image', 'once_published')
    actions = ['publish', 'unpublish']
    search_fields = ('title', 'content')
    save_as = True
    save_as_continue = True
    save_on_top = True

    fieldsets = (
        (_('Content part'), {
            'fields': (
                'title', 'slug', 'content',
                ('header_image', 'get_header_image'),
                ('post_image', 'get_post_image')
            )
        }),
        (_('Relation part'), {
            'fields': (
                'category', 'tags', 'is_published', 'once_published', 'author', 'views'
            )
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(author=request.user)

    def get_header_image(self, obj: object) -> str:
        return utils.get_image(obj.header_image, width=100, alt=_('Header image'))

    def get_post_image(self, obj: object) -> str:
        return utils.get_image(obj.post_image, width=100, alt=_('Post image'))

    def publish(self, request, queryset):
        """Publishes posts."""
        row_update = queryset.update(is_published=True)
        message = utils.staff_action_message(row_update)
        self.message_user(request, message)

    def unpublish(self, request, queryset):
        """Unpublishes posts."""
        row_update = queryset.update(is_published=False)
        message = utils.staff_action_message(row_update)
        self.message_user(request, message)

    publish.short_description = _('Publish')
    publish.allowed_permissions = ('change',)

    unpublish.short_description = _('Unpublish')
    unpublish.allowed_permissions = ('change',)

    get_header_image.short_description = _('Header image')
    get_post_image.short_description = _('Post image')


admin.site.site_title = _('News staff')
admin.site.site_header = _('News staff')
