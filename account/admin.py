from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.models.user import User
from .models.professional import Professional


@admin.register(User)
class UserAdminUser(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ('type', 'first_name', 'last_name', 'email', 'country', 'city', 'address')}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        'phone_number',
        'email',
        'date_of_birth',
        'image',
        'type',
        'first_name',
        'last_name',
        'country',
        'city',
        'address',
    )
    list_filter = ('phone_number', 'email', 'type', 'first_name', 'last_name', 'country', 'city', 'address')
    search_fields = ('phone_number', 'email')
    ordering = ('phone_number', )
    filter_horizontal = ()


@admin.register(Professional)
class UserAdminProfessional(UserAdmin):
    model = User
    fieldsets = (
        (None, {"fields": ()}),
        (_("Professional info"), {"fields": ('profession', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user__phone_number', 'user__password1', 'user__password2'),
        }),
    )
    list_display = ('get_phone_number', 'get_email', 'get_first_name', 'get_last_name', 'profession')
    list_filter = ('user__phone_number', 'user__email', 'user__first_name', 'user__last_name', 'profession')
    search_fields = ('user__phone_number', 'profession')
    ordering = ('user__phone_number', 'profession')
    filter_horizontal = ()
