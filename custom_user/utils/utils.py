from lab_manager_user.models import LabManager
from admin_user.serializers import AdminDetailSerializer
from lab_manager_user.serializers import LabManagerDetailSerializer
from custom_user.models import Role
from admin_user.models import Admin

class Util:
    @staticmethod
    def get_role_specific_details(user):
        details = None
        try:
            if(user.role == Role.ADMIN):
                serializer = AdminDetailSerializer(Admin.objects.get(user_ptr=user))
                details = serializer.data
            elif(user.role == Role.LAB_MANAGER):
                serializer = LabManagerDetailSerializer(LabManager.objects.get(user_ptr=user))
                details = serializer.data
        except:
            details=None
        return details
