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
    path('', views.profile, name="ShopHome"),
    path('myaddresses', views.address, name="addresses"),
    path('myorders', views.myorders, name="orders"),
    path('myreviews', views.myreviews, name="reviews"),
    path('addAddress', views.addAddress, name="addAddress"),
    path('deleteAddress/<int:id>', views.removeAddress, name="RemoveAddress"),
    path('addProduct', views.addProduct, name="addProduct"),
    path('defaultAddressChanged', views.defaultAddressChanged,
         name="defaultAddressChanged"),
    # path('myaddresses', views.address, name="ok"),
]
