from django.urls import path
from . import views

urlpatterns = [
    path('cart', views.cart, name='cart'),
    path('cart-json', views.cart_post, name='cart-json'),
]
