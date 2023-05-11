from rest_framework import serializers
from rest_framework.reverse import reverse

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password',
            'role',
        ]
        extra_kwargs = {'password': {'write_only': True}}
