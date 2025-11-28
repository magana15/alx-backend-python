from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp", "is_read")
    search_fields = ("sender__username", "receiver__username", "content")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "verb", "message", "is_read", "timestamp")
    list_filter = ("is_read",)
    search_fields = ("user__username", "verb")
