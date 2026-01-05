from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(
        max_length=11, 
        validators=[
            RegexValidator("^09\d{9}$", "Phone number must be entered in the format: '09xxxxxxxxx'.")
        ],
        verbose_name="Phone Number"
    )

    @property
    def role(self):
        if self.is_superuser:
            return 'admin'
        if self.groups.exists():
            return self.groups.first().name
        return 'normal'

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")


    objects = UserManager()

    def __str__(self):
        return self.username
    
