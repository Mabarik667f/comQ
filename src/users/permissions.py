from rest_framework import permissions


class IsOnlyOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        pass

