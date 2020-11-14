from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user

from src import utils
from src import validators
from email_notification import services
from users.models import UserModel


class PostCategoryModel(models.Model):
    """Category of post."""
    title = models.CharField(_('Title'), max_length=18, unique=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True,
                            help_text=_("Write nothing if you want to set slug field automatically"))
    image = models.ImageField(_('Image'), upload_to=utils.get_category_upload_path, blank=True,
                              help_text=_('Must be 1920x480px'), validators=[validators.validate_category_tag_image])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = utils.set_slug(self.title, self.slug)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['title']


class PostTagModel(models.Model):
    """Tag of post."""
    title = models.CharField(_('Title'), max_length=18, unique=True)
    slug = models.SlugField(_('Slug'), unique=True, blank=True,
                            help_text=_("Write nothing if you want to set slug field automatically"))
    image = models.ImageField(_('Image'), upload_to=utils.get_tag_upload_path, blank=True,
                              help_text=_('Must be 1920x480px'), validators=[validators.validate_category_tag_image])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = utils.set_slug(self.title, self.slug)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['title']


class PostModel(models.Model):
    """Post."""
    title = models.CharField(_('Title'), max_length=255, unique=True)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True, unique=True,
                            help_text=_("Write nothing if you want to set slug field automatically"))
    content = models.TextField(_('Content'))
    header_image = models.ImageField(_('Header image'), upload_to=utils.get_post_upload_path,
                                     help_text=_('Must be 1920x720px'), validators=[validators.validate_header_image]
                                     )
    post_image = models.ImageField(_('Post image'), upload_to=utils.get_post_upload_path,
                                   help_text=_('Must be 1200x800px'), validators=[validators.validate_post_image]
                                   )
    views = models.PositiveIntegerField(_('Views'), default=0)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='post_author', verbose_name=_('Author')
    )
    category = models.ForeignKey(
        PostCategoryModel, on_delete=models.PROTECT, related_name='post_category', verbose_name=_('Category')
    )
    tags = models.ManyToManyField(PostTagModel, related_name='post_tags', verbose_name=_('Tags'))
    is_published = models.BooleanField(_('Is published'), default=False)
    once_published = models.BooleanField(_('Once published'), default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts', kwargs={'slug': self.slug})

    def get_comment_list(self):
        return self.post_comment.all()

    def get_first_published_comment(self):
        return self.post_comment.earliest('created_at')

    def save(self, *args, **kwargs):
        self.slug = utils.set_slug(self.title, self.slug)
        if not hasattr(self, 'author'):
            # Adds authenticated user object to "author" field
            self.author = get_current_authenticated_user()
        if self.is_published and not self.once_published:
            # Makes "once_published" field in True if post was published at first time
            self.once_published = True
            services.notify_subscribers_new_post(self)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-created_at']


class PostViewsModel(models.Model):
    """Unique views of post by IP."""
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, verbose_name=_('Post'))
    ip = models.GenericIPAddressField('IP')
    datetime = models.DateTimeField(_('Datetime view'), auto_now_add=True, null=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = _('Post views')
        verbose_name_plural = _('Post views')


class PinnedPostModel(models.Model):
    """Pinned post."""
    pinned_post = models.OneToOneField(
        PostModel, unique=True, on_delete=models.CASCADE, related_name='pinned_posts', verbose_name=_('Post')
    )

    def __str__(self):
        return self.pinned_post.title

    def get_absolute_url(self):
        return reverse('posts', kwargs={'slug': self.pinned_post.slug})

    class Meta:
        verbose_name = _('Pinned post')
        verbose_name_plural = _('Pinned posts')
        ordering = ['-pinned_post__created_at']
