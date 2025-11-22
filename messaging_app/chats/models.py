import uuid
from django.conf import settings
from django.db import models

class Conversation(models.Model):
    """
    Conversation (thread) between two or more users.
    participants: ManyToMany -> settings.AUTH_USER_MODEL
    """
    conversation_id = models.UUIDField(
    primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="conversations",
        through="ConversationParticipant",
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
    fields=["created_at"], name="idx_conversation_created"),
        ]

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class ConversationParticipant(models.Model):
    """
    Optional through model for extra participant metadata (join timestamp, role in conversation, etc.)
    Keeps the many-to-many relation explicit and allows constraints or additional fields later.
    """
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(
    Conversation, on_delete=models.CASCADE, 
    related_name="participant_links")
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, related_name="conversation_links")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("conversation", "user")
        indexes = [
            models.Index(fields=["user"], name="idx_convpart_user"),
        ]

    def __str__(self):
        return f"{self.user} in {self.conversation}"

class Message(models.Model):
    """
    Message model containing sender FK, conversation FK, body, and timestamp.
    """
    message_id = models.UUIDField(
    primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(
    Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, related_name="sent_messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)    
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["sent_at"]
        indexes = [
            models.Index(fields=["sent_at"], name="idx_message_sent_at"),
            models.Index(fields=["conversation", "sent_at"], name="idx_message_conv_sent"),
        ]

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"

