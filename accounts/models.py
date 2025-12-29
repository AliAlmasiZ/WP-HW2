from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _





class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = 'admin', _('مدیر سامانه')
        SUPPORT = 'support', _('پشتیبان')
        PROVIDER = 'provider', _('پیمانکار')
        NORMAL = 'normal', _('کاربر عادی')

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.NORMAL,
        verbose_name=_('نقش کاربر')
    )
    

    def get_role_display(self):
        return self.UserRole(self.role).label
    

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
