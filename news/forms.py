from django import forms
from django.utils.translation import ugettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import PostModel, PinnedPostModel


class PinnedPostForm(forms.ModelForm):
    """The form of pinned posts."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Doesn't show news already added in hot news
        choices = [
            (post.pk, post) for post in PostModel.objects.all()
            if not PinnedPostModel.objects.filter(pinned_post_id=post.pk).exists()
        ]
        self.fields['pinned_post'].choices = (('', '---------'),)  # First empty value
        self.fields['pinned_post'].choices += choices


class PostAdminForm(forms.ModelForm):
    """CKEditor content form."""
    content_ru = forms.CharField(widget=CKEditorUploadingWidget, label=_('Content [ru]'), required=False)
    content_en = forms.CharField(widget=CKEditorUploadingWidget, label=_('Content [en]'))

    class Meta:
        model = PostModel
        fields = '__all__'
