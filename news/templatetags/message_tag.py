from django import template


register = template.Library()


@register.inclusion_tag('news/tags/message.html')
def show_message_from_level_important(messages):
    """Shows messages after submitting form."""
    context = {'messages': messages}
    return context
