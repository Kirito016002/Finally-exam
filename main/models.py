from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import os


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    quantitiy = models.DecimalField(decimal_places=2, max_digits=10)
    price = models.IntegerField()
    banner_image = models.ImageField(upload_to='product_image/baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    
    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.banner_image))
        if os.path.isfile(file_path):
            os.remove(file_path)
        super(Product, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Maxsulot"
        verbose_name_plural = "Maxsulotlar"
        
    def __str__(self):
        return self.title
    
    
class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_image/images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def delete(self, *args, **kwargs):
        file_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
        if os.path.isfile(file_path):
            os.remove(file_path)
        super(ProductImage, self).delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Maxsulot rasmi"
        verbose_name_plural = "Maxsulot rasmilari"
        
    def __str__(self):
        return self.product.title
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Savatcha"
        verbose_name_plural = "Savatchalar"
        
    def __str__(self):
        return self.user.username
    
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Savatchadagi maxsulot"
        verbose_name_plural = "Savatchadagi maxsulotlar"
        
    def __str__(self):
        return self.product.title
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    address = models.TextField()
    phone = models.CharField(max_length=255)
    order_type = models.SmallIntegerField(
        choices=(
            (0,'yetkazildi'), 
            (1, 'yo`lda'),
            (2, 'qaytarildi'),
            ), null=True, blank=True
    ) 
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        
    def __str__(self):
        return self.user.username
    
    

    
    



