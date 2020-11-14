from django import template
from django.core.cache import cache
from django.db.models import Count

from news.models import PostCategoryModel


register = template.Library()


@register.inclusion_tag('news/tags/category_list.html')
def show_category_list():
    """Shows all categories of published posts with total posts."""
    category_list = cache.get('category_list')
    if not category_list:
        category_list = PostCategoryModel.objects \
            .filter(post_category__is_published=True) \
            .annotate(count_published=Count('post_category')) \
            .filter(count_published__gt=0).order_by('-count_published')
        cache.set('category_list', category_list, 30)
    context = {'category_list': category_list}
    return context


@register.simple_tag
def get_category_list():
    """Returns all unique categories of published posts."""
    category_list = PostCategoryModel.objects \
        .filter(post_category__is_published=True) \
        .distinct()
    return category_list
