from django.db import models

# Create your models here.
class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        PENDING = "pending", "Pending"
        CLOSED = "closed", "Closed"

    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="tickets")
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name="Status")
    message = models.TextField("Message")
    answer = models.TextField("Answer", blank=True, null=True)
    related_ad = models.ForeignKey("ads.Ad", on_delete=models.SET_NULL, related_name="tickets", blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)
    class Meta:
        permissions = [
            ("can_answer_ticket", "Can answer tickets"),
            ("can_see_all_tickets", "Can see all tickets"),
        ]