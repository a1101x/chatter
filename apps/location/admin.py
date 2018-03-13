from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from mapwidgets.widgets import GooglePointFieldWidget

from apps.location.models import Location, Zipcode
from apps.user.admin import LocationInline


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {'widget': GooglePointFieldWidget}
    }
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Address'), {'fields': ('street', 'city', 'state', 'country',)}),
        (_('Zipcode'), {'fields': ('zipcode',)}),
        (_('Point'), {'fields': ('point',)})
    )
    raw_id_fields = ('user',)
    list_display = ('user', 'city', 'zipcode', 'point')
    search_fields = ('user__email', 'user__username', 'country', 'city', 'zipcode', 'state')
    ordering = ('user__username', 'user__email')


@admin.register(Zipcode)
class ZipcodeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Zipcode'), {'fields': ('code',)}),
        (_('Poly'), {'fields': ('poly',)})
    )
    inlines = (LocationInline,)
    list_display = ('code', 'poly')
    search_fields = ('code',)
    ordering = ('code',)
