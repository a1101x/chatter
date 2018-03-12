from django.contrib import admin
from django.utils.translation import ugettext as _

from apps.phone.models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Phone number'), {'fields': ('phone_number',)}),
        (_('Verified'), {'fields': ('is_verified',)})
    )
    raw_id_fields = ('user',)
    list_display = ('user', 'phone_number', 'is_verified')
    search_fields = ('user__email', 'user__username', 'phone_number')
    list_filter = ('is_verified',)
    ordering = ('user__email', 'user__username', 'phone_number')
