from django.contrib import admin
from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'ad', 'rate', 'created_at')
    list_filter = ('rate', 'created_at')
    search_fields = ('author__username', 'ad__title', 'content')
    ordering = ('-created_at',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'author',
                    'ad',
                    'content',
                    'rate',
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
                    'author',
                    'ad',
                    'content',
                    'rate',
                ),
                'classes': ('wide',)
            },
        ),
    )

    readonly_fields = (
        'created_at',
    )