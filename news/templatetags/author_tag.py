from django import template
from django.core.cache import cache


register = template.Library()


@register.inclusion_tag('news/tags/author_social_net_list.html')
def show_author_social_net_list(author):
    """Shows all social nets of author."""
    author_social_net_list = cache.get('author_social_net_list')
    if not author_social_net_list:
        fields = author.__dict__
        author_social_net_list = []
        for social_net_title, social_net_link in fields.items():
            if str(social_net_title).startswith('social') and social_net_link:
                social_net = {social_net_title.replace('social_', ''): social_net_link}
                author_social_net_list.append(social_net)
        cache.set('author_social_net_list', author_social_net_list, 30)
    context = {'author_social_net_list': author_social_net_list}
    return context
