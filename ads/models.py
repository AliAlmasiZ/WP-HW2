from django.db import models

# Create your models here.
class Ad(models.Model):
    class AdStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        ASSIGNED = 'assigned', 'Assigned'
        WAITING = 'waiting', 'Waiting for Confirmation'
        DONE = 'done', 'Done'
        CANCELLED = 'cancelled', 'Cancelled'
    title = models.CharField(max_length=200, verbose_name="Ad Title")
    description = models.TextField(verbose_name="Ad Description")
    category = models.CharField(max_length=100, verbose_name="Category")
    status = models.CharField(max_length=20, choices=AdStatus.choices, verbose_name="Ad Status")
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="Ad Owner")

    provider = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='provided_ads', verbose_name="Ad Provider")
    
    applicants = models.ManyToManyField(
        'accounts.User',
        related_name='applied_ads',
        blank=True,
        verbose_name="Applicants"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        permissions = [
            ("can_apply", "Can send application for an ad"),
            ("can_assign", "Can assign a provider to an ad"),
        ]

    def __str__(self):
        return self.title
    