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
    

# Product
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_image_create(request, pk):
    product = models.Product.objects.get(pk=pk)
    serializer = serialisers.ProductDetailImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_image_detail(request, pk):
    try:
        product = models.Product.objects.get(pk=pk)
        product_image = models.ProductImage.objects.get(pk=request.data.get('pk'), product=product)
    except models.ProductImage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = serialisers.ProductDetailImageSerializer(product_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product_image.delete()
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
    cart_products = models.CartProduct.objects.filter(cart = cart)
    if request.user == cart.user:
        serializer = serialisers.CartProductSerializer(cart_products, many=True)
        return Response(serializer.data)
    else:
        return Response(status.HTTP_404_NOT_FOUND)
    
    
# Cart product
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_create(request, pk):
    product = models.Product.objects.get(pk=pk)
    try:
        cart = models.Cart.objects.get(user=request.user, is_active=True)
        try:
            cart_product = models.CartProduct.objects.get(product=product)
            cart_product.quantity += 1
            cart_product.save()
            return Response(status.HTTP_200_OK)
        except:
            models.CartProduct.objects.create(
                cart=cart,
                product=product
            )
        return Response(status.HTTP_201_CREATED)   
    except:
        cart = models.Cart.objects.create(
            user=request.user
        )
        
        models.CartProduct.objects.create(
                cart=cart,
                product=product
            )
        return Response(status=status.HTTP_201_CREATED)

        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_delete(request, pk):
    product = models.Product.objects.get(pk=pk)
    cart = models.Cart.objects.get(user=request.user, is_active=True)
    cart_product = models.CartProduct.objects.get(product=product, cart=cart)
    if cart_product.quantity > 1:
        cart_product.quantity -= 1
        cart_product.save()
        serializer = serialisers.CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        cart_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# Order
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = models.Order.objects.all()
    serializer = serialisers.OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_create(request):
    user = request.user
    try:
        cart = models.Cart.objects.get(user=user, is_active=True)
        data = request.data.copy()
        
        data['user'] = user.pk
        data['cart'] = cart.pk

        serializer = serialisers.OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cart.is_active = not cart.is_active
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = models.Order.objects.get(pk=pk)
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serialisers.OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serialisers.OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)