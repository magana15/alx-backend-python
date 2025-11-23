from django.contrib import admin
from .models import Conversation, ConversationParticipant, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")
    #filter_horizontal = ("participants",)

@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    list_display = ("conversation", "user", "joined_at")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "conversation", "sender", "sent_at", "is_read")
    list_filter = ("is_read",)
    search_fields = ("message_body",)
