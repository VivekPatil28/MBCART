from operator import imod
from sre_constants import SUCCESS
from unicodedata import category
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse

from fuzzysearch import find_near_matches
from django.contrib import messages
# Create your views here.


# Home Page
def index(request):
    products = Product.objects.all()
    coursal = Coursal.objects.all()
    productimg = ProductImages.objects.all()
    
    StaticImages=StaticImage.objects.all()
    
    print(StaticImages)
    params = {'product': products,
              'coursal': coursal,
              'thumbnail': productimg,
              'StaticImages':StaticImages,
              }
    return render(request, 'shop\index.html', params)


#  Search functionality using fuzzysearch module
# tries to match the patterns and return response
def search(request):

    query = request.GET.get('search', '')
    query = query.strip()
    products = Product.objects.all()
    ids = set()
    query = query.lower()

    if (query == ""):
        return index(request)
    subcat = SubCategory.objects.all()
    products=Product.objects.all()
    for sc in subcat:
        s = find_near_matches(query, sc.name.lower(), max_l_dist=1)
        print(s)
        if (s != []):
            product = Product.objects.filter(Sub_Category_id=sc.id)
            for i in product:
                ids.add(i.product_id)
                print("ids "+ str(ids))

     # for product in products:
     #     subcat=SubCategory.objects.filter(id==product.Sub_Category_id)
     #     s = find_near_matches(query, subcat.lower(), max_l_dist=1)
     #     if (s != []):
     #         ids.add(product.product_id)

    # if (len(ids) == 0):
    #     for product in products:
    #         split_names = product.product_name.split(" ")
    #         split_names = split_names
    #         for word in split_names:
    #             s = find_near_matches(query, word.lower(), max_l_dist=1)
    #             if (s != []):
    #                 ids.add(product.product_id)
    

    params = {'query': query,
              'ids': ids,
              'product': products}
    return render(request, 'shop/searchResult.html', params)


# About section page
def about(request):

    return render(request, 'shop/about.html')


# Cart
def cart(request):
    pass


# contact page
def contact(request):
    return render(request, 'shop/contact.html', {"success": '0'})


# to submit the user response
def submitform(request):
    if (request.method == 'POST'):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phoneNumber = request.POST.get('phoneNumber', '')
        description = request.POST.get('description', '')
        contact = Contact(email=email, phoneNumber=phoneNumber,
                          description=description, name=name)
        contact.save()

        return render(request, 'shop/contact.html', {"success": '1'})


# profuct Description page
def product_desc(request, id):
    product = Product.objects.filter(product_id=id)[0]

    productimg = ProductImages.objects.filter(product_id=id)

    product_desc_imgs = ProductDescriptionImages.objects.filter(product_id=id)

    samecategory = (Product.objects.filter(
        Sub_Category_id = product.Sub_Category_id)).exclude(product_id=id)

    desc=product.product_desc
    desc=desc.split("$")
    
    
    Reviews = Review.objects.filter(product=product)
    
    
    ReviewImages = ReviewImage.objects.filter(product_id=product)
    
    params = {'product': product, 'sc': samecategory,
              'Reviews': Reviews, 'ReviewImages': ReviewImages, 'productimgs': productimg, 'product_desc': product_desc_imgs, 'aboutthisitem':desc}

    return render(request, 'shop/product_desc.html', params)


# Cart page
def AddToCart(request, id):
    return index(request)

# Signup


def signup(request):
    if request.method == 'POST':
        # we can also write like this
        # username=request.POST['username']
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, "Your Account has been successfully created.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if (user is not None):
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "Invalid Credentials")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def signout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def submitReview(request):
    if request.method == 'POST':
        imgs = request.FILES.getlist('imgs[]')
        username = request.POST['username']
        product_id = request.POST['product']
        rating=request.POST['rating']
        heading = request.POST['heading']
        body = request.POST['body']

        product = Product.objects.filter(product_id=product_id)[0]
        
        review = Review.objects.create(product=product,name=username, heading=heading,rating=rating, body=body)
        
        review.save()
        for img in imgs:
            ReviewImage.objects.create(
                image=img, review=review, product=product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def insertProduct(request):
    return render(request, 'shop/seller.html')

def liked(request):
    if request.method=='POST':
        reviewId=request.POST['reviewId']
        review= Review.objects.get(id=reviewId)
        review.likes=review.likes+1
        review.save()
        # data = {'likes':review.likes}
        # return JsonResponse(data, safe=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
