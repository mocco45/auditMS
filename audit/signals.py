# users/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserActionLog,minerals,mineralsYear,company

CustomUser = get_user_model()

@receiver(post_save, sender=CustomUser)
def log_user_save(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Updated'
    UserActionLog.objects.create(
        user=instance,
        action=f'{action} user',
        description=f'User {instance.email} was {action.lower()}.'
    )

@receiver(post_delete, sender=CustomUser)
def log_user_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted user',
        description=f'User {instance.email} was deleted.'
    )

# Repeat these signals for other models to capture their changes. For example:

@receiver(post_save, sender=minerals)
def log_some_other_model_save(sender, instance, created, **kwargs):
    action = 'Created' if created else 'Updated'
    UserActionLog.objects.create(
        user=instance,
        action=f'{action} some_other_model',
        description=f'SomeOtherModel with ID {instance.id} was {action.lower()}.'
    )

@receiver(post_delete, sender=minerals)
def log_user_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted user',
        description=f'User {instance.email} was deleted.'
    )

@receiver(post_delete, sender=company)
def log_some_other_model_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted some_other_model',
        description=f'SomeOtherModel with ID {instance.id} was deleted.'
    )
    
@receiver(post_delete, sender=company)
def log_user_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted user',
        description=f'User {instance.email} was deleted.'
    )
    
@receiver(post_delete, sender=mineralsYear)
def log_some_other_model_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted some_other_model',
        description=f'SomeOtherModel with ID {instance.id} was deleted.'
    )
    
@receiver(post_delete, sender=mineralsYear)
def log_user_delete(sender, instance, **kwargs):
    UserActionLog.objects.create(
        user=instance,
        action='Deleted user',
        description=f'User {instance.email} was deleted.'
    )
