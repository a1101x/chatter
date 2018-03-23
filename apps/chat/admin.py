from django.contrib import admin
from django.utils.translation import ugettext as _

from apps.chat.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff_only')
    fieldsets = (
        (_('Id'), {'fields': ('id',)}),
        (_('staff_only'), {'fields': ('staff_only',)})
    )
    readonly_fields = ('id',)
    search_fields = ('id',)
    list_filter = ('staff_only',)
