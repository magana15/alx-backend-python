from rest_framework.permissions import BasePermission
from rest_framework import permissions
class IsOwner(BasePermission):
    """
    Placeholder permission class.
    Currently allows all access;
    """
    def has_object_permission(self, request, view, obj):
        return True
