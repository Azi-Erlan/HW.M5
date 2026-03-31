
from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/categories/', views.category_list_api_view),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view),

    path('api/v1/products/', views.product_list_api_view),
    path('api/v1/products/<int:id>/', views.product_detail_api_view),

    path('api/v1/reviews/', views.review_list_api_view),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view),
]