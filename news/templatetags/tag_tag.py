from django import template

from news.models import PostTagModel


register = template.Library()


@register.simple_tag
def get_tag_list():
    """Returns tags of all published posts."""
    tag_list = PostTagModel.objects.filter(post_tags__is_published=True).distinct()
    return tag_list
