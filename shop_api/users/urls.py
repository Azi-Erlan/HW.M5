from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmUserAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
]