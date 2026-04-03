from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Avg, Count

from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryWithCountSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductReviewSerializer,
    ReviewListSerializer, ReviewDetailSerializer
)


@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = CategoryListSerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = CategoryDetailSerializer(category).data
    return Response(data=data)


@api_view(['GET'])
def category_with_count_api_view(request):
    categories = Category.objects.annotate(
        products_count=Count('products')
    )
    data = CategoryWithCountSerializer(categories, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = ProductDetailSerializer(product).data
    return Response(data=data)


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.prefetch_related('reviews').annotate(
        rating=Avg('reviews__stars')
    )

    data = ProductReviewSerializer(products, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewListSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = ReviewDetailSerializer(review).data
    return Response(data=data)