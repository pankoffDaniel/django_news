from modeltranslation.translator import register, TranslationOptions
from .models import PostCategoryModel, PostTagModel, PostModel


@register(PostCategoryModel)
class PostCategoryTranslationOptions(TranslationOptions):
    """Translation category of post."""
    fields = ('title',)


@register(PostTagModel)
class PostTagTranslationOptions(TranslationOptions):
    """Translation tag of post."""
    fields = ('title',)


@register(PostModel)
class PostTranslationOptions(TranslationOptions):
    """Translation of post."""
    fields = ('title', 'content')
