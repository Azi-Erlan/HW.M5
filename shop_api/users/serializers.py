from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode
from django.contrib.auth import get_user_model
import re

CustomUser = get_user_model()




class UserBaseSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=150)
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):

    def validate_email(self, email):
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('CustomUser уже существует!')
        return email

    def validate(self, attrs):
        phone = attrs.get("phone_number")

        if phone:
            if not phone.startswith("+996"):
                phone = "+996" + phone.lstrip("0")

            if not re.match(r'^\+996\d{9}$', phone):
                raise ValidationError("Неверный формат номера. Пример: +996700123456")

            attrs["phone_number"] = phone

        return attrs

class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('CustomUser не существует!')

        try:
            confirmation_code = ConfirmationCode.objects.get(user=user)
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Код подтверждения не найден!')

        if confirmation_code.code != code:
            raise ValidationError('Неверный код подтверждения!')

        return attrs