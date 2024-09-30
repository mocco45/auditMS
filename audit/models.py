from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class company(models.Model):
    name = models.CharField(max_length=255)

class minerals(models.Model):
    name = models.CharField(max_length=255)

class mineralsYear(models.Model):
    companie = models.ForeignKey(company, on_delete=models.CASCADE)
    mineral = models.ForeignKey(minerals, on_delete=models.CASCADE)
    year = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, photo=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, photo=photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, first_name, last_name, None, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserActionLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"
    
