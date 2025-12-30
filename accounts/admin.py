from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('created_at',)
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password',
                )
            },
        ),
        (
            'Personal info',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone_number',
                    'role',
                )
            }
        ),
        (
            'Permissions', 
            {
                'fields': (
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'groups', 
                    'user_permissions'
                )
                
            }
        ),
        (
            'System Information', 
            {
                'fields': (
                    'last_login',
                    'created_at',
                ),
                'classes': ('collapse',)
            }
        ),
    )
    
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'role',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_active',
                    'is_superuser',
                    'groups',
                )
            }
        ),
    )

    readonly_fields = (
        'created_at',
        'last_login'
    )

