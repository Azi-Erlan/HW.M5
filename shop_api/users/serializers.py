from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode


class RegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('User already exists!')


class ConfirmValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        user_id = data.get('user_id')
        code = data.get('code')

        try:
            confirmation = ConfirmationCode.objects.get(user_id=user_id)
        except:
            raise ValidationError('Code does not exist!')

        if confirmation.code != code:
            raise ValidationError('Invalid code!')

        return data