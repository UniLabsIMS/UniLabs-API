from admin_user.serializers import AdminDetailSerializer
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
        except:
            details=None
        return details
