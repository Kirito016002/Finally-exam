from django.urls import path

from . import views


urlpatterns = [
    # Category
    path('category-list/', views.category_list, name='category-list'),
    path('category-create/', views.category_create, name='category-create'),
    path('category-detail/<int:pk>', views.category_detail, name='category-detail'),
    # Product
    path('product-list/', views.product_list, name='product-list'),
    path('product-create/', views.product_create, name='product-create'),
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    #product
    path('product-image-create/<int:pk>', views.product_image_create, name='product-image-create'),
    path('product-image-detail/<int:pk>', views.product_image_detail, name='product-image-detail'),
    # Cart
    path('cart-list/', views.cart_list, name='cart-list'),
    path('cart-detail/<int:pk>', views.cart_detail, name='cart-detail'),
    # Cart product
    path('cart-product-create/<int:pk>', views.cart_product_create, name='cart-product-create'),
    path('cart-product-delete/<int:pk>', views.cart_product_delete, name='cart-product-delete'),
    # Order
    path('order-list/', views.order_list, name='order-list'),
    path('order-create/', views.order_create, name='order-create'),
    path('order-detail/<int:pk>', views.order_detail, name='order-detail'),
]