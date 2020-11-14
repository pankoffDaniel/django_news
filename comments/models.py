from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from news.models import PostModel
from users.models import UserModel


class PostCommentModel(MPTTModel):
    """Comment of post."""
    local_id = models.PositiveSmallIntegerField(_('Local id'), default=0)
    message = models.TextField(_('Comment'))

    comment_author = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name=_('Comment author'), related_name='comment_author')

    email = models.EmailField(_('Email'))
    name = models.CharField(pgettext_lazy('Contact form', 'Name'), max_length=30)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name=_('Parent comment'))
    post = models.ForeignKey(PostModel, related_name='post_comment', on_delete=models.CASCADE, verbose_name=_('Post'))
    is_deleted = models.BooleanField(_('Is deleted'), default=False)

    def __str__(self):
        return f'{self.name} - {self.post.title}'

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['created_at']

    class Meta:
        verbose_name = _('Post comment')
        verbose_name_plural = _('Post comments')
