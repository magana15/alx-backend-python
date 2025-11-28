from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notifications_on_message_save(sender, instance: Message, created: bool, **kwargs):
    """
    When a new Message is created, create Notification(s) for all conversation participants
    except the sender.
    """
    if not created:
        return

    message = instance
    sender_user = message.sender

    # try to get participants from the conversation
    try:
        participants_qs = message.conversation.participants.all()
    except Exception:
        participants_qs = []

    summary = (message.message_body[:200]) if getattr(message, "message_body", None) else ""

    notifications = []
    for recipient in participants_qs:
        if recipient == sender_user:
            continue
        notifications.append(Notification(
            user=recipient,
            message=message,
            text=summary,
        ))

    if notifications:
        Notification.objects.bulk_create(notifications)
