from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *  # Optional, if you have additional fields


UserAdmin = BaseUserAdmin
UserAdmin.fieldsets[1][1]['fields'] = ('first_name', 'last_name', 'email')  # enable email editing




User = get_user_model()

# Optional: Unregister default User model only if previously registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Customize as needed
    list_display = ['email', 'is_active', 'is_staff']
    search_fields = ['email']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )