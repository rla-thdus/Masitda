from rest_framework.permissions import BasePermission


class IsOwnerOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == '사장'
