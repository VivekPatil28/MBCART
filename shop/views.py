from itertools import product
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from UserProfile.models import Address
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
    category=Category.objects.all()
    cart=""
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)

    StaticImages = StaticImage.objects.all()

    print(StaticImages)
    params = {'product': products,
              'coursal': coursal,
              'thumbnail': productimg,
              'StaticImages': StaticImages,
              'cart':cart,
              'category':category,
              }
    return render(request, 'shop\index.html', params)


#  Search functionality using fuzzysearch module
# tries to match the patterns and return response
def search(request):

    query = request.GET.get('search', '')
    query = query.strip()
    ids = set()
    query = query.lower().replace(" ", "")
    print(query)

    if (query == ""):
        return index(request)

    category = Category.objects.all()
    subcat = SubCategory.objects.all()
    products = Product.objects.all()
    for cat in category:
        s = find_near_matches(query, cat.name.lower(), max_l_dist=0)
        print(s)
        if (s != []):
            product = Product.objects.filter(Category_id=cat.id)
            for i in product:
                ids.add(i.product_id)
                print("ids 1st " + str(ids))  # for view

    for sc in subcat:
        s = find_near_matches(query, sc.name.lower(), max_l_dist=0)
        print(s)
        if (s != []):
            product = Product.objects.filter(Sub_Category_id=sc.id)
            for i in product:
                ids.add(i.product_id)
                print("ids 2nd " + str(ids))

    if (len(ids) == 0):
        for product in products:
            split_names = product.product_name.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                print(s)
                if (s != []):
                    ids.add(product.product_id)

        for product in products:
            split_names = product.product_desc.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                print(s)
                if (s != []):
                    ids.add(product.product_id)

    params = {'query': query,
              'ids': ids,
              'product': products}
    return render(request, 'shop/searchResult.html', params)


# About section page
def about(request):

    return render(request, 'shop/about.html')


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
    product = Product.objects.get(product_id=id)
    sub_cat = SubCategory.objects.get(id=product.Sub_Category_id)
    productimg = ProductImages.objects.filter(product_id=id)
    product_desc_imgs = ProductDescriptionImages.objects.filter(product_id=id)
    samecategory = (Product.objects.filter(
        Category_id=product.Category_id)).exclude(product_id=id)

    desc = product.product_desc
    desc = desc.split("\n")

    what_is_in_the_box = product.what_is_in_the_box
    what_is_in_the_box = what_is_in_the_box.split("\n")

    Reviews = Review.objects.filter(product=product)
    user_review = Reviews.filter(user_id=request.user.id)

    is_added_to_cart = False

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        for item in cart:
            if product == item.product:
                is_added_to_cart = True

    total_ratings = 0

    for r in Reviews:
        total_ratings += r.rating

    if (len(Reviews) > 0):
        product_rating = total_ratings/len(Reviews)
    else:
        product_rating = 0

    product.product_rating = product_rating
    product.save(force_update=True)

    ReviewImages = ReviewImage.objects.filter(product_id=product)

    params = {'product': product, 'sc': samecategory, 'user_review': user_review, 'sub_cat': sub_cat, 'is_added_to_cart': is_added_to_cart,
              'Reviews': Reviews, 'ReviewImages': ReviewImages, 'productimgs': productimg, 'product_desc': product_desc_imgs, 'aboutthisitem': desc, 'what_is_in_the_box': what_is_in_the_box}

    return render(request, 'shop/product_desc.html', params)


# Cart page
def AddToCart(request, id):
    if request.method == 'GET':
        product = Product.objects.get(product_id=id)
        cartitem, is_added = Cart.objects.get_or_create(
            user=request.user, product=product, totalprice=product.product_price)
        getCartItems(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removecartitem(request):
    if request.method == 'POST':
        id = request.POST['id']
        Cart.objects.filter(id=id).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    cartitems = Cart.objects.filter(user=request.user)
    d_address= Address.objects.get(user=request.user, default_address=True)
    params = {
        'cartitems': cartitems,
        'd_address':d_address,
    }
    return render(request, 'shop/cart.html', params)


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
        return HttpResponseRedirect('/')


def submitReview(request):
    if request.method == 'POST':
        imgs = request.FILES.getlist('imgs[]')
        username = request.POST['username']
        product_id = request.POST['product']
        rating = request.POST['rating']
        heading = request.POST['heading']
        body = request.POST['body']

        product = Product.objects.filter(product_id=product_id)[0]

        review = Review.objects.create(user=request.user,
                                       product=product, name=username, heading=heading, rating=rating, body=body)

        review.save()
        for img in imgs:
            ReviewImage.objects.create(
                image=img, review=review, product=product)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def insertProduct(request):
    return render(request, 'shop/seller.html')


def liked(request):
    if request.method == 'POST':
        reviewId = request.POST['reviewId']
        review = Review.objects.get(id=reviewId)
        review.likes = review.likes+1
        review.save()
        # data = {'likes':review.likes}
        # return JsonResponse(data, safe=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def disliked(request):
    if request.method == 'POST':
        reviewId = request.POST['reviewId']
        review = Review.objects.get(id=reviewId)
        review.dislikes = review.dislikes+1
        review.save()
        # data = {'likes':review.likes}
        # return JsonResponse(data, safe=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def category(request, string):
    cat = Category.objects.get(name=string)
    products = Product.objects.filter(Category_id=cat.id)
    params = {'products': products}
    return render(request, 'shop/category_desc.html', params)

def subcategory(request,string):
    scat=SubCategory.objects.get(name=string)
    products = Product.objects.filter(Sub_Category=scat)
    return render(request,'shop/category_desc.html',{'products':products})
    


def getCartItems(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            data = Cart.objects.filter(user_id=request.user.id)
            cartitems = {'num': len(data)}
            return JsonResponse(cartitems, safe=False)


def payment(request):
    return render(request, 'shop/paymentGateway.html')