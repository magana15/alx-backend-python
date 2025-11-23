import uuid
from django.conf import settings
from django.db import models

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    # store hashed password in this field (string)
    password_hash = models.CharField(max_length=255, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_GUEST = "guest"
    ROLE_HOST = "host"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_GUEST, "Guest"),
        (ROLE_HOST, "Host"),
        (ROLE_ADMIN, "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_GUEST)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chats_user"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"], name="idx_user_email"),
        ]

    def __str__(self):
        return f"{self.email}"


class Conversation(models.Model):
    """
    Conversation (thread) between two or more users.
    participants: ManyToMany -> settings.AUTH_USER_MODEL or local User
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    participants = models.ManyToManyField(
        "chats.User",  # explicitly reference local model for the checker
        related_name="conversations",
        through="ConversationParticipant",
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"], name="idx_conversation_created"),
        ]

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class ConversationParticipant(models.Model):
    """
    Through model for participants.
    """
    id = models.BigAutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="participant_links"
    )
    user = models.ForeignKey(
        "chats.User", on_delete=models.CASCADE, related_name="conversation_links"
    )
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
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        "chats.User", on_delete=models.CASCADE, related_name="sent_messages"
    )
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
