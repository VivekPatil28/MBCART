from http.client import HTTPResponse
from django.shortcuts import render
import UserProfile
from shop import models as model
from .models import *


def profile(request):
    return render(request, 'UserProfile/profile.html')

def address(request):
    address= Address.objects.filter(user=request.user)
    print(address)
    return render(request, 'UserProfile/address.html',{'address':address})

def myorders(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'UserProfile/myorders.html',{'orders':orders})
def myreviews(request):
    reviews=model.Review.objects.filter(user=request.user)
    reviewImages=model.ReviewImage.objects.all()
    
    params={
        'reviews':reviews,
        'ReviewImages': reviewImages
    }
    return render(request,'UserProfile/myreviews.html',params)

def addAddress(request):
    if request.method == 'POST':
        name=request.POST['fullname']
        number=request.POST['number']
        alternateNumber=request.POST['alternateNumber']
        state = request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']
        houseno=request.POST['houseno']
        area=request.POST['area']
        homeaddress=request.POST.get('addresstype')
        
        print(homeaddress)
        address, is_added =Address.objects.get_or_create(user=request.user,full_name=name,phone_number=number,alternate_phone_number=alternateNumber,pincode=pincode,
                                                         state=state, city=city, house_no=houseno, area=area, home_work_address=homeaddress)
        
        
        
    return render(request,'UserProfile/addAddress.html')


    