from django.contrib import admin
from django.utils.translation import ugettext as _

from apps.mailer.models import EmailTemplate


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('key', 'subject', 'created_at', 'updated_at', 'is_active')
    fieldsets = (
        (_('Key'), {'fields': ('key',)}),
        (_('Email'), {'fields': ('subject', 'title', 'body', 'button_label', 'button_link', 'is_active')}),
        (_('Date'), {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('key', 'subject', 'title', 'body')
