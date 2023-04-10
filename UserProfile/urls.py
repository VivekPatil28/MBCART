from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path("", views.profile, name="ShopHome"),
    path("myaddresses", views.address, name="addresses"),
    path("myorders", views.myorders, name="orders"),
    path("myreviews", views.myreviews, name="reviews"),
    path("myaddresses/addAddress", views.addAddress, name="addAddress"),
    path("deleteAddress/<int:id>", views.removeAddress, name="RemoveAddress"),
    path("addProduct", views.addProduct, name="addProduct"),
    path("contact",views.contact,name="contact"),
    path("cancelOrder/<int:id>",views.cancelOrder,name="cancelOrder"),
    path(
        "defaultAddressChanged",
        views.defaultAddressChanged,
        name="defaultAddressChanged",
    ),
    # path('myaddresses', views.address, name="ok"),
]
