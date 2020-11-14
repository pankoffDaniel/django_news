from django import template

from comments.forms import PostCommentForm


register = template.Library()


@register.simple_tag
def get_comment_captcha_form():
    return PostCommentForm()
