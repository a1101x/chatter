from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from mapwidgets.widgets import GooglePointFieldInlineWidget

from apps.location.models import Location
from apps.phone.models import Phone
from apps.user.models import ChangeEmailCode, User, UserActivationCode

admin.site.site_header = 'Chatter'
admin.site.index_title = 'Admin Panel'
admin.site.site_url = ''
admin.site.unregister(Group)


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0


class LocationInline(admin.StackedInline):
    model = Location
    extra = 0
    formfield_overrides = {
        models.PointField: {'widget': GooglePointFieldInlineWidget}
    }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (PhoneInline, LocationInline)
    fieldsets = (
        (_('User'), {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'birthday')}),
        (_('Gender'), {'fields': ('gender',)}),
        (_('Photo'), {'fields': ('photo',)}),
        (_('Permissions'), {
            'classes': ('collapse',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')
        }),
        (_('Important dates'), {
            'classes': ('collapse',),
            'fields': ('last_login', 'date_joined')
        })
    )
    list_display = ('username', 'email', 'gender', 'is_active', 'last_login')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('username', 'email', 'last_login')
    list_filter = ('gender', 'groups', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)

            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)

        obj.save()


@admin.register(UserActivationCode)
class UserActivationCodeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Code'), {'fields': ('code',)}),
        (_('Times'), {'fields': ('time_expired', 'created')})
    )
    list_display = ('user', 'code', 'time_expired', 'created')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('user', 'code', 'time_expired', 'created')
    list_filter = ('user__is_active',)
    ordering = ('user__email',)


@admin.register(ChangeEmailCode)
class ChangeEmailCodeAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Code'), {'fields': ('code',)}),
        (_('New email'), {'fields': ('new_email',)}),
        (_('Times'), {'fields': ('time_expired', 'created')})
    )
    list_display = ('user', 'new_email', 'code', 'time_expired', 'created')
    search_fields = ('user__email', 'user__username', 'new_email')
    list_filter = ('user__is_active',)
    readonly_fields = ('user', 'new_email', 'code', 'time_expired', 'created')
    ordering = ('user__email',)
