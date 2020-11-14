from django import template

from news.models import PostModel


register = template.Library()


@register.simple_tag
def get_popular_post_list(end):
    """Returns {end} the most popular posts."""
    return PostModel.objects.filter(is_published=True) \
        .select_related('category') \
        .order_by('-views')[:end]


@register.inclusion_tag('news/tags/post_list.html')
def show_post_list(post_list):
    """Shows posts."""
    return {'post_list': post_list}


@register.inclusion_tag('news/tags/pagination.html')
def show_pagination_panel(page_obj, search=''):
    """Shows pagination panel."""
    return {'page_obj': page_obj, 'search': search}
