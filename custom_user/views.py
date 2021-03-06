from custom_user.models import User
from custom_user.serializers import ChangePasswordSerializer, LoginSerializer, RefreshAuthSerializer, ResetPasswordSerializer, UpdateProfileDetailsSerializer, UserBlockUnblockSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

# API end point for user login
class UserLoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API endpoint to change user password
class ChangePasswordAPIView(GenericAPIView):
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)
        

        def post(self, request, *args, **kwargs):
            user = self.request.user
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check current password
                if not user.check_password(serializer.data.get("current_password")):
                    return Response({"current_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                user.set_password(serializer.data.get("new_password"))
                if(user.is_default_password):user.is_default_password=False
                user.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API end point to edit profile details
class UpdateProfileDetialsAPIView(GenericAPIView):
    serializer_class = UpdateProfileDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        user = self.request.user
        serializer = self.get_serializer(data=request.data,partial=True,instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Refresh User Auth with token
class RefreshUserAuthAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshAuthSerializer

    def get(self,request):
        serializer = self.serializer_class(data={'user':request.user},context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


# API end point to block a user
class BlockUnblockAPIView(GenericAPIView):
    serializer_class = UserBlockUnblockSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    queryset = User.objects.all()
    lookup_field='id'

    def put(self,request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data,instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API end point to block a user
class ResetPasswordAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        

    

    
