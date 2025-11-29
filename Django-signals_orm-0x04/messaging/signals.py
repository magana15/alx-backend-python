from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_old_content(sender, instance: Message, **kwargs):
    """
    Before a Message is saved, if it already exists in DB and its content is changing,
    store the old content in MessageHistory.

    If the view has set instance._edited_by (a convention we use below), we store that as editor.
    """
    if instance.pk is None:
        return

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content == instance.content:
        return

    editor = getattr(instance, "_edited_by", None)

    def _create_history():
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            edited_at=timezone.now(),
            editor=editor
        )

        instance.edited = True
        instance.edited_at = timezone.now()

    transaction.on_commit(_create_history)
