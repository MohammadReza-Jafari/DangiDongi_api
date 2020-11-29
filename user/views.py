from rest_framework import generics

from . import serializers


class RegisterUser(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer