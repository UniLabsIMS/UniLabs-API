from custom_user.serializers import LoginSerializer
from rest_framework import generics,status
from rest_framework.response import Response

# API end point for user login
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
