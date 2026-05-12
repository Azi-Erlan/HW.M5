from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView
from .google_oauth import GoogleOAuthAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),

    path('google-login/', GoogleOAuthAPIView.as_view()),
]