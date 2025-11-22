from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only requests (GET, HEAD, OPTIONS) if user is participant
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()
        
        # Allow write requests (POST, PUT, PATCH, DELETE) only if user is participant
        return request.user in obj.participants.all()
