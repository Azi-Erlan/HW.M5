import random
import string

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ConfirmationCode
from .serializers import (
    AuthValidateSerializer,
    ConfirmationSerializer,
    RegisterValidateSerializer,
    CustomTokenObtainPairSerializer,
)
from django.core.cache import cache
from users.tasks import add, send_otp_email

CustomUser = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):

        # from time import sleep

        # sleep(15)

        add.delay(8,2)
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"error": "CustomUser account is not activated yet!"},
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={"key": token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={"error": "CustomUser credentials are wrong!"},
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        birthdate = serializer.validated_data["birthdate"]

        # Use transaction to ensure data consistency
        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email, 
                password=password, 
                birthdate=birthdate,
                is_active=True
            )

            # Create a random 6-digit code
            code = "".join(random.choices(string.digits, k=6))

            cache.set(
                f"confirmation_code_{user.id}",
                code,
                timeout=300
            )
            send_otp_email.delay(email=email, otp=code)

        return Response(
            status=status.HTTP_201_CREATED,
            data={"user_id": user.id, "confirmation_code": code},
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmationSerializer

    def post(self, request):
        serializer = ConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        code = serializer.validated_data["code"]

        saved_code = cache.get(f"confirmation_code_{user_id}")

        if saved_code != code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "Неверный код подтверждения"},
            )

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            cache.delete(f"confirmation_code_{user.id}")
            
        return Response(
            status=status.HTTP_200_OK,
            data={
                "message": "CustomUser аккаунт успешно активирован",
                "key": token.key,
            },
        )