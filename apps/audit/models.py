from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.accounts.models import CustomUser


class UserActionLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"
