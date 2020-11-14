from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from comments import services as comment_services
from .models import PostCommentModel
from .forms import PostCommentForm
from email_notification.tasks import send_mail_function
from news import services as post_services


def add_comment(request):
    """Adds comment to post."""
    if request.method != 'POST':
        raise PermissionDenied()
    form = PostCommentForm(request.POST)
    if not form.is_valid():
        messages.error(request, _('Please check Email correct or try later'))
        return redirect(request.META.get('HTTP_REFERER'))
    pk = request.POST.get('post_id')

    try:
        post_slug = post_services.get_post_slug_by_pk(pk)
    except ObjectDoesNotExist:
        messages.error(request, 'Post ID does not exist')
        return redirect(request.META.get('HTTP_REFERER'))

    comment_list_count = comment_services.get_comment_list_count_by_post_pk(pk)
    if comment_list_count.get('local_id__max'):
        local_id = comment_list_count['local_id__max'] + 1
    else:
        local_id = 1
    parent_id = request.POST.get('parent')

    form = form.save(commit=False)
    form.local_id = local_id
    form.post_id = pk
    if request.user.is_authenticated:
        form.comment_author = request.user

    if parent_id:
        try:
            parent_comment = comment_services.get_parent_post_comment_by_pk(parent_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Parent comment ID does not exist')
            return redirect(request.META.get('HTTP_REFERER'))

        form.parent_id = int(parent_id)
        send_from = settings.EMAIL_HOST_USER

        email_list = [parent_comment.email if parent_comment else parent_comment.comment_author.email]
        subject = 'Your comment was answered'
        message = f'Follow link belong to see reply on your comment.\n' \
                  f'Link: {settings.DOMAIN_URL}/posts/{post_slug}/#{local_id}'
        send_mail_function.delay(subject, message, send_from, email_list, countdown=60 * 5, max_retries=3)

    form.save()
    messages.success(request, _('Your comment has been posted!'))
    return redirect(request.META.get('HTTP_REFERER'))


def action_comment(request):
    """Makes selected action with post comment."""
    if request.method != 'POST':
        raise PermissionDenied()
    if request.POST.get('hide_comment'):
        comment = PostCommentModel.objects.get(id=request.POST.get('hide_comment'))
        comment.is_deleted = True
        comment.save()
    return redirect(request.META.get('HTTP_REFERER'))
