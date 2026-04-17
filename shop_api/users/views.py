from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random

from .models import ConfirmationCode
from .serializers import RegisterValidateSerializer, ConfirmValidateSerializer


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            username=request.data.get('username'),
            password=request.data.get('password'),
            is_active=False
        )

        code = str(random.randint(100000, 999999))
        ConfirmationCode.objects.create(user=user, code=code)

        return Response({'user_id': user.id, 'code': code}, status=201)


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = User.objects.get(id=serializer.validated_data.get('user_id'))
        user.is_active = True
        user.save()

        ConfirmationCode.objects.filter(user=user).delete()

        return Response({'status': 'confirmed'})


class AuthorizationAPIView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'key': token.key})

        return Response(status=401)