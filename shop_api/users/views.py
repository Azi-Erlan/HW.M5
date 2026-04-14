from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random

from .models import ConfirmationCode
from .serializers import RegisterValidateSerializer, ConfirmValidateSerializer


@api_view(['POST'])
def registration_api_view(request):
    # step 1: validation
    serializer = RegisterValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # step 2: receive data
    username = request.data.get('username')
    password = request.data.get('password')

    # step 3: create user
    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )

    # step 4: generate code
    code = str(random.randint(100000, 999999))

    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    # step 5: return response
    return Response(
        status=status.HTTP_201_CREATED,
        data={
            'user_id': user.id,
            'code': code
        }
    )


@api_view(['POST'])
def confirm_api_view(request):
    # step 1: validation
    serializer = ConfirmValidateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors
        )

    user_id = serializer.validated_data.get('user_id')

    # step 2: activate user
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()

    # step 3: delete code
    ConfirmationCode.objects.filter(user_id=user_id).delete()

    return Response(
        status=status.HTTP_200_OK,
        data={'status': 'confirmed'}
    )


@api_view(['POST'])
def authorization_api_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)

        return Response(data={'key': token.key})

    return Response(status=status.HTTP_401_UNAUTHORIZED)