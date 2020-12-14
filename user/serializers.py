import re
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext as _
from rest_framework_jwt.settings import api_settings

from wallet.serializers import WalletSerializer

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'profile_image', 'phone_number', 'password')
        extra_kwargs = {
            'password': {
                'min_length': 5,
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'error_messages': {
                    'blank': 'ایمیل را وارد کنید.',
                    'unique': 'کاربری با این ایمیل موجود می باشد.'
                }
            },
            'first_name': {
                'error_messages': {
                    'max_length': 'نام نهایتا می تواند 30 کاراکتر باشد.',
                    'blank': 'نام را وارد کنید.'
                }
            },
            'last_name': {
                'error_messages': {
                    'max_length': 'نام خانوادگی نهایتا می تواند 50 کاراکتر باشد.',
                    'blank': 'نام خانوادگی را وارد کنید.'
                }
            },
            'phone_number': {
                'error_messages': {
                    'max_length': 'ماره تلفن نهایتا می تواند 13 کاراکتر باشد.'
                }
            },
            'profile_image': {
                'error_messages': {
                    'invalid_extension': 'فقط فایل های با پسوند jpg و png و jpeg قابل قبول می باشند'
                }
            }
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user

    def validate_phone_number(self, value):
        if not value:
            return value
            # raise serializers.ValidationError(
            #     _('شماره تلفن را وارد کنید.')
            # )
        if not re.match(
            pattern="(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}",
            string=value
        ):
            raise serializers.ValidationError(
                _('شماره تلفن وارد شده معتبر نمی باشد.'),
                code='invalid'
            )
        return value


class EditUserSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(slug_field='amount', read_only=True)
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'profile_image', 'phone_number', 'wallet')
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'blank': 'ایمیل را وارد کنید.',
                    'unique': 'کاربری با این ایمیل موجود می باشد.'
                }
            },
            'first_name': {
                'error_messages': {
                    'max_length': 'نام نهایتا می تواند 30 کاراکتر باشد.',
                    'blank': 'نام را وارد کنید.'
                }
            },
            'last_name': {
                'error_messages': {
                    'max_length': 'نام خانوادگی نهایتا می تواند 50 کاراکتر باشد.',
                    'blank': 'نام خانوادگی را وارد کنید.'
                }
            },
            'phone_number': {
                'error_messages': {
                    'max_length': 'ماره تلفن نهایتا می تواند 13 کاراکتر باشد.'
                }
            },
            'profile_image': {
                'error_messages': {
                    'invalid_extension': 'فقط فایل های با پسوند jpg و png و jpeg قابل قبول می باشند'
                }
            },
            'wallet': {
                'read_only': True
            }
        }

    def validate_phone_number(self, value):
        if not value:
            return value
            # raise serializers.ValidationError(
            #     _('شماره تلفن را وارد کنید.')
            # )
        if not re.match(
            pattern="(0|\+98)?([ ]|-|[()]){0,2}9[1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}",
            string=value
        ):
            raise serializers.ValidationError(
                _('شماره تلفن وارد شده معتبر نمی باشد.'),
                code='invalid'
            )
        return value


class UserTokenSerializer(serializers.Serializer):

    class Meta:
        fields = ('email', 'password', 'token')
        extra_kwargs = {
            'password': {
                'style': {
                    'input_type': 'password'
                },
                'min_length': 5,
                'write_only': True,
                'error_message': {
                    'required': 'رمزعبور را وارد کنید'
                }
            },
            'email': {
                'error_message': {
                    'required': 'ایمیل را وارد کنید'
                }
            }
        }

    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                'کاربر با این اطلاعات پیدا نشد.',
                code='INVALID_CREDENTIAL'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'حساب کاربری شما فعال نمی باشد',
                code='USER_NOT_ACTIVE'
            )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except get_user_model().DoesNotExists:
            raise serializers.ValidationError(
                'کاربر با ایمیل داده شده پیدا نشد.',
                code='INVALID_CREDENTIAL'
            )

        return {
            'email': user.email,
            'token': token
        }


class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        fields = ('old_password', 'new_password')
        extra_kwargs = {
            'old_password': {
                'min_length': 5,
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'new_password': {
                'min_length': 5,
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        fields = ('reset_code', 'new_password')
        extra_kwargs = {
            'new_password': {
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                },
                'write_only': True,
                'error_messages': {
                    'required': 'رمز جدید را وارد کنید',
                    'min_length': 'رمز باید بیشتر از 5 کاراکتر باشد'
                }
            }
        }
    reset_code = serializers.IntegerField(required=True)
    new_password = serializers.CharField(min_length=5, required=True)