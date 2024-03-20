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
    # Cart
    path('cart-list/', views.cart_list, name='cart-list'),
    path('cart-detail/<int:pk>', views.cart_detail, name='cart-detail'),
]