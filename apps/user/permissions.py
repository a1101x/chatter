from rest_framework import permissions


class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow access on PATCH/PUT only for account owner.
    """
    message = 'Only account owner can edit profile.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user == obj
        )
