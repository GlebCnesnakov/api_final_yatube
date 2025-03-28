from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        a = obj.author == request.user
        b = request.method in permissions.SAFE_METHODS
        return a or b


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        a = request.method in permissions.SAFE_METHODS
        b = request.method == 'POST'
        return a or b
