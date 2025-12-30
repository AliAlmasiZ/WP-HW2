from django.db import models

# Create your models here.
class Ad(models.Model):
    class AdStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        DONE = 'done', 'Done'
        PENDING = 'pending', 'Pending'
    title = models.CharField(max_length=200, verbose_name="Ad Title")
    description = models.TextField(verbose_name="Ad Description")
    category = models.CharField(max_length=100, verbose_name="Category")
    status = models.CharField(max_length=20, choices=AdStatus.choices, verbose_name="Ad Status")
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="Ad Owner")

    provider = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='provided_ads', verbose_name="Ad Provider")
    

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")


    def __str__(self):
        return self.title
