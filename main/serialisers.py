from rest_framework import serializers
from . import models

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Category
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Category
        fields = '__all__'
        
    def get_products(self, cat):
        products = models.Product.objects.filter(category=cat)
        serializer = ProductSerializer(products, many=True)
        return serializer.data
    
    
class ProductDetailImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'image',]    


class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Product
        fields = '__all__'
        
    def get_product_images(self, product):
        product_images = models.ProductImage.objects.filter(product=product)
        serializer = ProductDetailImageSerializer(product_images, many=True)
        return serializer.data
    
    
class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = models.CartProduct
        fields = ['id', 'quantity', 'product']
        
        
class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Cart
        fields = ['id', 'is_active']