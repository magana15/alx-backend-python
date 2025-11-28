from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance: Message, created, **kwargs):
    """
    When a new Message is created, create a Notification for the receiver.
    Use transaction.on_commit to avoid creating notifications for rolled-back transactions.
    """
    if not created:
        return

    # ensure message save transaction has committed before creating the notification
    def _create_notification():
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            verb="sent you a message"
        )
    transaction.on_commit(_create_notification)
