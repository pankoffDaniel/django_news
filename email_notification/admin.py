from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import MailUsAdminForm
from .models import EmailSubscriptionModel, MailUsModel


@admin.register(EmailSubscriptionModel)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    """Admin form of email subscription."""
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')
    fields = ('email',)


@admin.register(MailUsModel)
class MailUsAdmin(admin.ModelAdmin):
    """Admin form of Mail Us."""
    form = MailUsAdminForm
    list_display = ('id', 'email', 'question_subject', 'answer_staff', 'is_answered')
    list_display_links = ('id', 'email', 'question_subject')
    fieldsets = (
        (_('Guest'), {
            'fields': (
                'email', 'question_subject', 'question_message'
            )
        }),
        (_('Staff'), {
            'fields': (
                'answer_subject', 'answer_message', 'answer_staff', 'is_answered'
            )
        }),
    )
    readonly_fields = ('email', 'question_subject', 'question_message', 'answer_staff', 'is_answered')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        """Allows to change row if field "is_answered" is empty."""
        if obj:
            return not obj.is_answered
        return False

    def has_delete_permission(self, request, obj=None):
        """Superuser can delete users' letters."""
        if request.user.is_superuser:
            return True
        return False
