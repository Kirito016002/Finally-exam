from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from . import models, serialisers

# 0f8e67a8cb37edd8bfbf2b2c50f59c099faa326b
# db82e40698c22d2b12c5841dd365da16f3de96b7


# Categoriya
@api_view(['GET'])
def category_list(request):
    categories = models.Category.objects.all()
    serializer = serialisers.CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_create(request):
    serializer = serialisers.CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try:
        category = models.Category.objects.get(pk=pk)
    except models.Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serialisers.CategoryWithProductsSerializer(category)
        print(serializer)
        return Response(serializer.data)

    elif request.method == 'PUT': 
        serializer = serialisers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# Product
@api_view(['GET'])
def product_list(request):
    products = models.Product.objects.all()
    serializer = serialisers.ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_create(request):
    user = request.user
    serializer = serialisers.ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = models.Product.objects.get(pk=pk)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serialisers.ProductDetailSerializer(product)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serialisers.ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# Cart
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_list(request):
    carts = models.Cart.objects.filter(user=request.user)
    serializer = serialisers.CartSerializer(carts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request, pk):
    cart = models.Cart.objects.get(pk = pk)
    if request.user == cart.user:
        serializer = serialisers.CartProductSerializer(cart, many=True)
        return Response(serializer.data)
    else:
        return Response(status.HTTP_404_NOT_FOUND)