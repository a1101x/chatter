from rest_framework import permissions


class IsPhoneNumberOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow access on PATCH/PUT/DELETE only for phone number owner.
    """
    message = 'Only phone number owner can edit phone.'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user == obj.user
        )
