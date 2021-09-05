from rest_framework import permissions
from .models import Student
from custom_user.permissions import IsAdmin
from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import StudentReadSerializer, StudentRegisterSerializer
from rest_framework.permissions import IsAuthenticated

# Student Register View
class StudentRegisterAPIView(generics.GenericAPIView):
    serializer_class = StudentRegisterSerializer
    permission_classes = (IsAuthenticated,IsAdmin) # Only admins may add students

    def post(self,request): # post request to register new student
        student = request.data
        serializer = self.serializer_class(data=student)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        student_data = serializer.data        
        return Response(student_data,status=status.HTTP_201_CREATED)

# GET request to get all lab students in the system as a list
class AllStudentsAPIView(generics.ListAPIView):
    serializer_class=StudentReadSerializer
    queryset=Student.objects.all()
    permission_classes=(permissions.IsAuthenticated,IsAdmin)