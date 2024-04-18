"""
Django admin customization
"""

from django.contrib import admin

# UserAdmin is used for customizing and managing the admin site(admin interface) for user model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# it will import all models that we want to register
from core import models

from django.utils.translation import (
    gettext_lazy as _,
)  # this line can be used for future for translation text


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    # we need to specify ordering because by default it uses username which we do not have in our custom model and if we do not specify it will throw error
    ordering = ["id"]
    list_display = ["email", "name"]

    # the below changes are for the screen for http://127.0.0.1:8000/admin/core/user/1/change/
    # we will specify fieldset that we have created in our custom model
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(
    models.User, UserAdmin
)  # need to add custom admin class to display accordingly
# it registers the "User" model with with the UserAdmin class to enable custom admin interface configuration for user management
