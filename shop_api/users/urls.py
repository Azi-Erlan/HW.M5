from django.urls import path
from .views import RegistrationAPIView, AuthorizationAPIView, ConfirmAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('authorization/', AuthorizationAPIView.as_view()),
    path('confirm/', ConfirmAPIView.as_view()),
]