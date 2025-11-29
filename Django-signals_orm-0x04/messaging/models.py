from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Conversation(models.Model):
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or f"Conversation {self.pk}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
        help_text="If set, this message is a reply to parent_message"
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True
    )
    verb = models.CharField(max_length=255, default="sent you a message")
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Notification for {self.user}: {self.verb}"

class MessageHistory(models.Model):
    """
    Stores previous versions of a Message's content.
    Created *before* a Message is updated.
    """
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    # editor is optional because in signals we may not always have access to the request user
    editor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="edited_histories"
    )

    class Meta:
        ordering = ["-edited_at"]

    def __str__(self):
        return f"History for message {self.message_id} at {self.edited_at}"
