from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission

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
    def create_user(self, username, email, first_name, last_name, photo, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, photo=photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='photos/')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name