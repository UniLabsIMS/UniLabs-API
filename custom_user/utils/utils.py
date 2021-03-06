from lecturer_user.models import Lecturer
from lecturer_user.serializers import LecturerDetailSerializer
from student_user.models import Student
from student_user.serializers import StudentDetailSerializer
from lab_assistant_user.models import LabAssistant
from lab_manager_user.models import LabManager
from admin_user.serializers import AdminDetailSerializer
from lab_manager_user.serializers import LabManagerDetailSerializer
from custom_user.models import Role
from admin_user.models import Admin
from decouple import config

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
            elif(user.role == Role.LAB_ASSISTANT):
                serializer = LabManagerDetailSerializer(LabAssistant.objects.get(user_ptr=user))
                details = serializer.data
            elif(user.role == Role.STUDENT):
                serializer = StudentDetailSerializer(Student.objects.get(user_ptr=user))
                details = serializer.data
            elif(user.role == Role.LECTURER):
                serializer = LecturerDetailSerializer(Lecturer.objects.get(user_ptr=user))
                details = serializer.data
        except:
            details=None
        return details

    
    
