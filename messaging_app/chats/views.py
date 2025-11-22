from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    List / Retrieve / Create / Update / Destroy conversations.
    - List: returns conversations the request.user participates in.
    - Create: accepts `title` and `participant_ids` (list of user PKs/UUIDs).
      The creating user is always added as a participant.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show only conversations where the requesting user is a participant
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def get_serializer_class(self):
        # use a compact serializer for list and full serializer for retrieve/create
        if self.action == "list":
            return ConversationListSerializer
        return ConversationDetailSerializer

    def perform_create(self, serializer):
        # serializer.create() in ConversationDetailSerializer already handles participant_ids,
        # but ensure the creating user is a participant
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)
        # Optionally update updated_at or notify participants here
        return conversation

    def create(self, request, *args, **kwargs):
        """
        Override to return HTTP 201 with the serialized conversation detail
        and to surface validation errors cleanly.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        convo = self.perform_create(serializer)
        out_serializer = ConversationDetailSerializer(convo, context={"request": request})
        headers = self.get_success_headers(out_serializer.data)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["get"], url_path="messages", url_name="messages")
    def list_messages(self, request, pk=None):
        """
        Optional helper endpoint: GET /api/conversations/{pk}/messages/
        Returns messages for conversation (paginated if you enable pagination globally).
        """
        convo = self.get_object()
        # ensure requesting user is participant
        if request.user not in convo.participants.all():
            return Response({"detail": "Not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        qs = convo.messages.all().order_by("sent_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = MessageSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    List / Retrieve / Create messages.
    - List: returns messages in conversations the user participates in.
    - Create: requires `conversation` and `message_body`. Sender is set to request.user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Messages only from conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user).distinct()

    def perform_create(self, serializer):
        # Ensure sender is request.user and that user is a participant of the conversation
        request = self.request
        conversation = serializer.validated_data.get("conversation")
        if conversation is None:
            raise serializers.ValidationError({"conversation": "This field is required."})

        # Ensure the user is a participant of the conversation; if not, deny or auto-add depending on your policy.
        if request.user not in conversation.participants.all():
            # Option A: deny sending
            raise permissions.PermissionDenied("You are not a participant in this conversation.")

            # Option B (alternative): automatically add the user as participant
            # conversation.participants.add(request.user)

        serializer.save(sender=request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create to enforce the serializer context and return created message.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
