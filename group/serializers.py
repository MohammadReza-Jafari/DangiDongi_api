from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Group


class CreateGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'admin')
        read_only_fields = ('id', 'admin')

        extra_kwargs = {
            'title': {
                'error_messages': {
                    'blank': 'نام گروه نمی تواند خالی باشد',
                    'max_length': 'نام گروه از 250 کاراکتر بیشتر نمی تواند باشد'
                }
            }
        }


class GroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title')


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'nick_name', 'email', 'profile_image')


class GroupDetailsSerializer(serializers.ModelSerializer):
    admin = UserDetailsSerializer()
    members = UserDetailsSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'


