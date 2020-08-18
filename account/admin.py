from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_admin', 'is_staff', 'last_login', 'date_joined')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            "fields": (
                'email', 'username'
            ),
        }),
        ('Permissions', {
            "fields": (
                'is_admin', 'is_staff'
            )
        }),
        ('Read Only Fields', {
            "fields": (
                'date_joined', 'last_login'
            )
        })
    )

    add_fieldsets = (
        (None, {
            "fields": (
                'email', 'username', 'password1', 'password2'
            ),
        }),
    )

    list_filter = ('date_joined',)

    filter_horizontal = ()
    
admin.site.register(Account, CustomUserAdmin)