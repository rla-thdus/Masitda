from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.role == '사장':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsMine(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
