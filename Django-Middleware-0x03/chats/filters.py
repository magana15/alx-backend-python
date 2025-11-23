import django_filters
from django_filters import rest_framework as filters
from .models import Message

class MessageFilter(filters.FilterSet):
    """
    Filter messages by:
      - conversation id (UUID string)
      - sender id (UUID string)
      - message text contains (icontains)
      - sent_at range: after / before
    """
    conversation = filters.UUIDFilter(field_name="conversation__conversation_id", lookup_expr="exact")
    sender = filters.UUIDFilter(field_name="sender__user_id", lookup_expr="exact")
    message_body = filters.CharFilter(field_name="message_body", lookup_expr="icontains")
    sent_after = filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        # These are the filter names the API will accept as query params
        fields = ["conversation", "sender", "message_body", "sent_after", "sent_before"]
