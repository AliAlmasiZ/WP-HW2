from django.contrib import admin
from .models import Ticket

# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("owner", "status", "related_ad", "created_at")
    list_filter = ("owner", "status")
    search_fields = ("onwer", )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "status",
                    "message",
                    "answer",
                    "related_ad",
                )
            }
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            }
        )
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "status",
                    "message",
                    "answer",
                    "related_ad",
                )
            }
        ),
    )

    readonly_fields = (
        "created_at", 
    )