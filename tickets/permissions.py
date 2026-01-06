from rest_framework import permissions

class canAnswerTicket(permissions.BasePermission):
    """
    Custom permission to only allow users with 'can_answer_ticket' permission to answer tickets.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.has_perm('tickets.can_answer_ticket') or request.user.is_superuser
    
class canEditTicket(permissions.BasePermission):
    """
    Custom permission to only allow ticket owners or users with 'can_answer_ticket' permission to edit tickets.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.owner == request.user:
            return True

        return request.user.has_perm('tickets.can_answer_ticket') or request.user.is_superuser