"""MBCART URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from xml.etree.ElementInclude import include
from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about', views.about, name="About"),
    path('cart', views.cart, name="Cart"),
    path('contact', views.contact, name="contact"),
    path('submitform', views.submitform, name="submitform"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('submitReview', views.submitReview, name="submitReview"),
    path('insertProduct', views.insertProduct, name="insertProduct"),
    path('searchResult', views.search, name="search"),
    path('product/<int:id>', views.product_desc, name="product_desc"),
    path('AddToCart/<int:id>', views.AddToCart, name="addtocart"),
    path('liked', views.liked, name="liked"),
    path('disliked', views.disliked, name="disliked"),
    path('removecartitem', views.removecartitem, name="removecartitem"),
    path('category/<str:string>', views.category, name="category_desc"),
    path('subcategory/<str:string>', views.subcategory, name="sub_cat_desc"),
    path('getCartItems', views.getCartItems, name="getCartItems"),
    path('payment', views.payment, name="payment"),
   
    # path('checkout', views.checkout, name="checkout"),
]
