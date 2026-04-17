from django.urls import path
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ReviewViewSet,
    CategoryCountAPIView,
    ProductReviewAPIView
)

urlpatterns = [
    # CATEGORY
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('categories/<int:id>/', CategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('categories/count/', CategoryCountAPIView.as_view()),

    # PRODUCT
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:id>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('products/reviews/', ProductReviewAPIView.as_view()),

    # REVIEW
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:id>/', ReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]