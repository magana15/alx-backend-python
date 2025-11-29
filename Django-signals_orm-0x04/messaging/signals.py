from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from .models import Message, MessageHistory, Notification

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

@receiver(pre_save, sender=Message)
def log_message_old_content(sender, instance: Message, **kwargs):
    # only interested in updates to existing messages
    if instance.pk is None:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # if content unchanged, do nothing
    if old.content == instance.content:
        return

    # editor convention set by the view: instance._edited_by
    editor = getattr(instance, "_edited_by", None)

    def _create_history():
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_at=timezone.now(),
            editor=editor
        )

        # update instance so the save persists these values
        instance.edited = True
        instance.edited_at = timezone.now()
        # set the foreign key on the message to point to the latest editor
        instance.edited_by = editor

    transaction.on_commit(_create_history)
