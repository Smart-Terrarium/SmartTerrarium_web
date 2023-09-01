from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User

"""Admin panel changes"""


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    # Define the fieldsets for user information
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # Define the fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # Display these fields in the list view of users
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    # Enable searching for users by these fields
    search_fields = ('email', 'first_name', 'last_name')
    # Set the default ordering for users
    ordering = ('email',)
