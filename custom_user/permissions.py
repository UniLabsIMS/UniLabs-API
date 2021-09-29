 
from rest_framework import permissions
from .models import Role
from lab_assistant_user.models import LabAssistant
from lab_manager_user.models import LabManager

# Class to check whether the current user is an admin
class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN


# Class to check whether the current user is a lab manager
class IsLabManager(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.LAB_MANAGER


# Class to check whether the current user is a lab assistant
class IsLabAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.LAB_ASSISTANT

# Class to check whether the current user is a lab assistant or lab manager
class IsLabManagerOrAssistant(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.role == Role.LAB_ASSISTANT) or (request.user.role == Role.LAB_MANAGER)


# Class to check whether the user is a student

class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.STUDENT

class IsLecturer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == Role.LECTURER

class IsLabOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.user.role == Role.LAB_ASSISTANT):
            assistant = LabAssistant.objects.get(id=request.user.id)
            if(assistant.lab==obj.lab):
                return True
            else:
                return False
        if(request.user.role == Role.LAB_MANAGER):
            manager = LabManager.objects.get(id=request.user.id)
            if(manager.lab==obj.lab):
                return True
            else:
                return False
        return False