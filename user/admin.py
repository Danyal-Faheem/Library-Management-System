from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, UserProfile


class CustomUserAdmin(UserAdmin):
    """CustomUserAdmin to include our extra fields on admin panel"""

    # Override fieldsets to include email and role on panel
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),)

    # Override add_fieldsets to include email and role in add_user section of admin panel
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "role"),
            },
        ),
    )


""" 
Register our own model against the UserAdmin to utilize 
the Django admin panel and provide necessary permissions
"""
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
