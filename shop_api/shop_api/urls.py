
from django.contrib import admin
from django.urls import path, include
from . import swagger
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/products/', include('product.urls')),   
    path('api/v1/users/', include('users.urls')), 
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
]

urlpatterns += swagger.urlpatterns