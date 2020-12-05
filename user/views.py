from rest_framework import generics, permissions, status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from . import serializers


class RegisterUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class LoginUserView(generics.RetrieveAPIView):

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserTokenSerializer

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            response = {
                'success': True,
                'data': ser.data,
                'message': 'کاربر با موفقیت پیدا شد.',
                'status_code': status.HTTP_200_OK
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class GetProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.UserSerializer
    authentication_class = JSONWebTokenAuthentication

    def get_object(self):
        return self.request.user
