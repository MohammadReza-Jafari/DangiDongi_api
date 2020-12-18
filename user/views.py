from rest_framework import generics, permissions, status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import Http404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from random import randint

from . import serializers


class RegisterUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class LoginUserView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
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
    """
    token needed
     * pattern is "Bearer token-value"
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.EditUserSerializer
    authentication_class = JSONWebTokenAuthentication

    def get_object(self):
        return self.request.user


class ActivateUserView(APIView):

    @swagger_auto_schema(
        operation_description='فعالسازی حساب کاربری',
        responses={
            status.HTTP_200_OK: 'successful activation',
            status.HTTP_404_NOT_FOUND: 'wrong activation code'
        }
    )
    def get(self, request, code):
        try:
            user = get_object_or_404(get_user_model(), activation_code=code)
            user.is_active = True
            user.activation_code = None
            user.save()
            response = {
                'success': True,
                'status': status.HTTP_200_OK,
                'message': f'حساب کاربری با ایمیل{user.email}فعال شد'
            }
            return Response(response, status=status.HTTP_200_OK)
        except Http404:
            response = {
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'کد فعالسازی اشتباه می باشد'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    @swagger_auto_schema(
        request_body=serializers.ChangePasswordSerializer,
        operation_description="تغییر رمز حساب کاربری\n\n"
                              "token needed\n * pattern is 'Bearer token-value' in header",
        responses={
            status.HTTP_200_OK: 'every thing okay',
            status.HTTP_400_BAD_REQUEST: 'something is wrong'
        }
    )
    def post(self, request):
        ser = serializers.ChangePasswordSerializer(data=request.data)

        if ser.is_valid():
            user = request.user

            if not user.check_password(ser.validated_data.get('old_password')):
                response = {
                    'success': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'رمز فعلی صحیح نمی باشد.'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if ser.validated_data['old_password'] == ser.validated_data['new_password']:
                response = {
                    'success': False,
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'رمز فعلی و رمز جدید یکسان می باشند'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(ser.validated_data['new_password'])
            user.save()

            response = {
                'success': True,
                'message': 'با موفقیت رمز عوض شد.',
                'status': status.HTTP_200_OK
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class GetResetCodeView(APIView):

    @swagger_auto_schema(
        operation_description='درخواست فراموشی رمز عبور',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, pattern='example@example.com')
            },
            required=['email']
        ),
        responses={
            status.HTTP_200_OK: 'reset code will send to user email',
            status.HTTP_400_BAD_REQUEST: 'wrong email',
        }
    )
    def post(self, request):
        email = request.data.get('email', None)

        if not email:
            response = {
                'success': False,
                'message': 'ایمیل نمی تواند خالی باشد',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
            try:
                user = get_object_or_404(get_user_model(), email=email)
                reset_code = randint(100000, 999999)
                user.reset_code = reset_code
                user.save()
                # i should implement sending reset code to user email
                return Response('okay')
            except Http404:
                response = {
                    'success': False,
                    'message': 'کاربری با این ایمیل یافت نشد.',
                    'status': status.HTTP_404_NOT_FOUND
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
            response = {
                'success': False,
                'message': 'ایمیل وارد شده معتبر نمی باشد',
                'status': status.HTTP_400_BAD_REQUEST
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):

    @swagger_auto_schema(
        request_body=serializers.ResetPasswordSerializer,
        operation_description='تغییر رمز کاربر با استفاده از کد و رمز جدید',
        responses={
            status.HTTP_200_OK: 'رمز با موفقیت تفییر کرد',
            status.HTTP_400_BAD_REQUEST: 'اشتباهی رخ داده است',
            status.HTTP_404_NOT_FOUND: 'کاربری با ایم کد وجود ندارد'
        }
    )
    def post(self, request):
        ser = serializers.ResetPasswordSerializer(data=request.data)

        if ser.is_valid():
            try:
                user = get_object_or_404(
                    get_user_model(),
                    reset_code=ser.validated_data.get('reset_code', None)
                )

                user.reset_code = None
                user.set_password(ser.validated_data.get('new_password', None))
                user.save()

                response = {
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': 'رمز با موفقیت تغییر کرد'
                }
                return Response(response, status=status.HTTP_200_OK)
            except Http404:
                response = {
                    'success': False,
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'کاربری با این کد یافت نشد'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
