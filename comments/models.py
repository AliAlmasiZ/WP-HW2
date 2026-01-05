from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name="Comment Author")
    content = models.TextField(verbose_name="Comment Content")
    rate = models.IntegerField(
        verbose_name="Comment Rate",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ad = models.ForeignKey('ads.Ad', on_delete=models.CASCADE, verbose_name="Related Ad", related_name="comments")
    provider = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name="Provider", related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

