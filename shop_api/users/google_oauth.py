import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.serializers import OAuthCodeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.timezone import now


User = get_user_model()


class GoogleOAuthAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']

        token_response = requests.post(
            url='https://oauth2.googleapis.com/token',
            data={
                'code': code,
                'client_id': '807695682244-il3qt23mr7illasr2uqb7vn88mmpn6rt.apps.googleusercontent.com',
                # 'client_secret': 'YOUR_CLIENT_SECRET',
                'redirect_uri': 'http://localhost:8000/api/v1/users/google-login/',
                'grant_type': 'authorization_code',
            }
        )

        token_data = token_response.json()
        print(token_data)
        access_token = token_data.get('access_token')

        if not access_token:
            return Response({'error': 'Invalid access token: '})
        
        user_info = requests.get(
            url='https://www.googleapis.com/oauth2/v3/userinfo',
            params={'alt': 'json'},
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        print(f'USER_INFO: {user_info}')

        email = user_info['email']

        if not email:
            return Response(
                {'error': 'Email not found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'registration_source': 'google'
            }
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name

        user.is_active = True
        user.last_login = now()

        user.save()

        refresh = RefreshToken.for_user(user)
        refresh['email'] = user.email

        return Response(
            {
                'access_token': str(refresh.access_token), 
                'refresh_token': str(refresh)
            }
        )