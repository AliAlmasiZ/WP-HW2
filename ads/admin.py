from django.contrib import admin
from .models import Ad


# Register your models here.
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title',)
    ordering = ('-created_at',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'description',
                    'category',
                    'status',
                )
            },
        ),
        (
            'System Information', 
            {
                'fields': (
                    'created_at',
                ),
                'classes': ('collapse',)
            }
        )
    )

    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'title',
                    'description',
                    'category',
                    'status',
                ),
                'classes': ('wide',)
            },
        ),
    )

    readonly_fields = (
        'created_at',
    )

