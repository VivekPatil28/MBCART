from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
import UserProfile
from shop import models as model
from .models import *


# from django.shortcuts import render, redirect
# from .models import *
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login, logout
# import json
# from django.http import JsonResponse

# from fuzzysearch import find_near_matches
# from django.contrib import messages

# Create your views here.


def profile(request):
    # address=Address.objects.get(user=request.user,default_address=True)
    return render(request, 'UserProfile/profile.html')


def address(request):
    address = Address.objects.filter(user=request.user)
    return render(request, 'UserProfile/address.html', {'address': address})


def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by("-order_date")
    print(orders)
    return render(request, 'UserProfile/myorders.html', {'orders': orders})


def myreviews(request):
    reviews = model.Review.objects.filter(user=request.user)
    reviewImages = model.ReviewImage.objects.all()

    params = {
        'reviews': reviews,
        'ReviewImages': reviewImages
    }
    return render(request, 'UserProfile/myreviews.html', params)


def addAddress(request):
    if request.method == 'POST':
        name = request.POST['fullname']
        number = request.POST['number']
        alternateNumber = request.POST['alternateNumber']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        houseno = request.POST['houseno']
        area = request.POST['area']
        homeaddress = request.POST.get('addresstype')

        address, is_added = Address.objects.get_or_create(user=request.user, full_name=name, phone_number=number, alternate_phone_number=alternateNumber, pincode=pincode,
                                                          state=state, city=city, house_no=houseno, area=area, home_work_address=homeaddress)
    
    
    return render(request,"UserProfile/addAddress.html")


def removeAddress(request, id):
    Address.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def addProduct(request):
    return render(request,'UserProfile/addProduct.html')


def defaultAddressChanged(request):
    if request.method == 'POST':
        addressId = request.POST['check']
        print(addressId)
        user_address=Address.objects.filter(user=request.user)
        for add in user_address:
            add.default_address=False
            add.save()
        address=Address.objects.get(id=addressId)
        address.default_address=True
        address.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
