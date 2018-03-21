from django.contrib import admin
from django.utils.translation import ugettext as _

from apps.messenger.models import SMSTemplate


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ('key', 'body', 'created_at', 'updated_at', 'is_active')
    fieldsets = (
        (_('Key'), {'fields': ('key',)}),
        (_('Email'), {'fields': ('body', 'is_active')}),
        (_('Date'), {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('key', 'body')
