import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


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