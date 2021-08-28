 
from rest_framework import permissions
from .models import Role

# Class to check whether the current user is an admin
class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


# Class to check whether the current user is a lab manager
class IsLabManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.LAB_MANAGER