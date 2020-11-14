from django import template
from django.core.cache import cache

from settings import services


register = template.Library()


@register.simple_tag
def get_social_net_list():
    """Returns all social nets of site."""
    social_net_list = cache.get('social_net_list')
    if not social_net_list:
        social_net_list = services.get_site_social_net_list()
        cache.set('social_net_list', social_net_list, 30)
    return social_net_list


@register.simple_tag
def get_site_settings():
    """Returns main settings of site."""
    main_settings = cache.get('main_settings')
    if not main_settings:
        main_settings = services.get_site_mail_settings()
        cache.set('main_settings', main_settings, 30)
    return main_settings
