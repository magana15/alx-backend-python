import uuid
from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Conversation, Message, ConversationParticipant
from users.serializers import UserSerializer

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    - sender is set/read-only (the view or HiddenField populates it).
    """
    sender = UserSerializer(read_only=True)  # nested read representation
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="sender", required=False
    )

    class Meta:
        model = Message
        fields = ("message_id", "conversation", "sender", "sender_id", "message_body", "sent_at", "is_read")
        read_only_fields = ("message_id", "sent_at", "sender", "is_read")

    def create(self, validated_data):
        # If view sets request.user via context, prefer that; otherwise allow sender_id write
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["sender"] = request.user
        return super().create(validated_data)


class ConversationParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for the through model (if you want to show joined_at, etc.)
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source="user"
    )

    class Meta:
        model = ConversationParticipant
        fields = ("id", "conversation", "user", "user_id", "joined_at")
        read_only_fields = ("id", "joined_at", "user")


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Lightweight Conversation serializer for list views:
    - participants shown as nested users
    - messages not included (keeps list endpoints light)
    """
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ("conversation_id", "title", "participants", "created_at")
        read_only_fields = ("conversation_id", "created_at")


class ConversationDetailSerializer(serializers.ModelSerializer):
    """
    Full Conversation serializer for retrieve endpoints:
    - includes nested participants and messages (read-only).
    - Use pagination for the messages endpoint in production to avoid huge responses.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)   # uses related_name="messages"

    # write-only field to accept participant IDs when creating/updating
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Conversation
        fields = ("conversation_id", "title", "participants", "participant_ids", "messages", "created_at")
        read_only_fields = ("conversation_id", "participants", "messages", "created_at")

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids", [])
        conversation = Conversation.objects.create(**validated_data)
        if participant_ids:
            conversation.participants.set(participant_ids)
        return conversation

    def update(self, instance, validated_data):
        participant_ids = validated_data.pop("participant_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if participant_ids is not None:
            instance.participants.set(participant_ids)
        return instance
