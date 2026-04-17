from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count

from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryWithCountSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductReviewSerializer,
    ReviewListSerializer, ReviewDetailSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
)



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action in ['create', 'update']:
            return CategoryValidateSerializer
        return CategoryDetailSerializer

    def perform_create(self, serializer):
        Category.objects.create(**serializer.validated_data)

    def perform_update(self, serializer):
        category = self.get_object()
        category.name = serializer.validated_data.get('name')
        category.save()



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update']:
            return ProductValidateSerializer
        return ProductDetailSerializer

    def perform_create(self, serializer):
        Product.objects.create(**serializer.validated_data)

    def perform_update(self, serializer):
        product = self.get_object()
        for field, value in serializer.validated_data.items():
            setattr(product, field, value)
        product.save()



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action in ['create', 'update']:
            return ReviewValidateSerializer
        return ReviewDetailSerializer

    def perform_create(self, serializer):
        Review.objects.create(**serializer.validated_data)

    def perform_update(self, serializer):
        review = self.get_object()
        for field, value in serializer.validated_data.items():
            setattr(review, field, value)
        review.save()



class CategoryCountAPIView(APIView):
    def get(self, request):
        categories = Category.objects.annotate(products_count=Count('products'))
        return Response(CategoryWithCountSerializer(categories, many=True).data)



class ProductReviewAPIView(APIView):
    def get(self, request):
        products = Product.objects.prefetch_related('reviews').annotate(
            rating=Avg('reviews__stars')
        )
        return Response(ProductReviewSerializer(products, many=True).data)