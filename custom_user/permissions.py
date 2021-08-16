 
from rest_framework import permissions
from .models import Role

# Class to check whther the current user is an admin
class IsAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.role == Role.ADMIN