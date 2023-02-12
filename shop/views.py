from itertools import product
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import date
from UserProfile.models import Address
from UserProfile.models import Order
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from fuzzysearch import find_near_matches
from django.contrib import messages
# Create your views here.


# Home Page
def index(request):
    products = Product.objects.all()
    coursal = Coursal.objects.all()
    productimg = ProductImages.objects.all()
    category = Category.objects.all()
    latest_laptops = Product.objects.filter(
        Category_id=5).order_by('-product_publish_date').values()
    latest_mobiles = Product.objects.filter(
        Category_id=1).order_by('-product_publish_date').values()
    latest_headphones = Product.objects.filter(
        Category_id=2).order_by('-product_publish_date').values()
    cart = ""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
    StaticImages = StaticImage.objects.all()
    params = {'product': products,
              'coursal': coursal,
              'thumbnail': productimg,
              'StaticImages': StaticImages,
              'cart': cart,
              'category': category,
              'latest_laptops': latest_laptops,
              'latest_mobiles': latest_mobiles,
              'latest_headphones': latest_headphones,
              }

    if request.COOKIES.get('recentitems'):
        recent_items = eval(request.COOKIES.get('recentitems'))
        params['recent_items'] = recent_items[6::-1]

    if request.COOKIES.get('recentsearch'):
        recent_search = eval(request.COOKIES.get('recentsearch'))
        params['recent_search'] = recent_search[:6]

    return render(request, 'shop\index.html', params)


#  Search functionality using fuzzysearch module
# tries to match the patterns and return response
def search(request):

    query = request.GET.get('search', '')
    query = query.strip()
    ids = set()
    query = query.lower().replace(" ", "")

    if (query == ""):
        return index(request)

    category = Category.objects.all()
    subcat = SubCategory.objects.all()
    products = Product.objects.all()
    for cat in category:
        s = find_near_matches(query, cat.name.lower(), max_l_dist=0)
        if (s != []):
            product = Product.objects.filter(Category_id=cat.id)
            for i in product:
                ids.add(i.product_id)

    for sc in subcat:
        s = find_near_matches(query, sc.name.lower(), max_l_dist=0)
        if (s != []):
            product = Product.objects.filter(Sub_Category_id=sc.id)
            for i in product:
                ids.add(i.product_id)

    if (len(ids) == 0):
        for product in products:
            split_names = product.product_name.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                if (s != []):
                    ids.add(product.product_id)

        for product in products:
            split_names = product.product_desc.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                if (s != []):
                    ids.add(product.product_id)

    # Only the result objects
    qs = Product.objects.none()
    for i in ids:
        qs = qs | Product.objects.filter(product_id=i)

    params = {'query': query,
              'ids': ids,
              'product': qs}
    response = render(request, 'shop/searchResult.html', params)
    # For recent search items
    # response.delete_cookie('recentsearch')
    if not request.COOKIES.get('recentsearch'):
        response.set_cookie('recentsearch', str(list(ids)))
    else:
        arr = eval(request.COOKIES.get('recentsearch'))
        for i in ids:
            if i not in arr:
                arr.append(i)
        response.set_cookie('recentsearch', str(arr))

    return response


# About section page
def about(request):

    return render(request, 'shop/about.html')


# contact page
def contact(request):
    return render(request, 'shop/contact.html', {"success": '0'})


# to submit the user response
def submitform(request):
    if (request.method == 'POST'):
        try:
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phoneNumber = request.POST.get('phoneNumber', '')
            description = request.POST.get('description', '')
            contact = Contact(email=email, phoneNumber=phoneNumber,
                            description=description, name=name)
            contact.save()
            messages.success(request, "Address Successfully Added")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")

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

    product_tech_d =[]
    details=product.product_techinical_details
    for i in details.split("\n"):
        product_tech_d.append(i.split("\t"))
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

    params = {'product': product,
              'sc': samecategory,
              'user_review': user_review,
              'sub_cat': sub_cat,
              'is_added_to_cart': is_added_to_cart,
              'Reviews': Reviews,
              'ReviewImages': ReviewImages,
              'productimgs': productimg,
              'product_desc': product_desc_imgs,
              'aboutthisitem': desc,
              'techinical_details':product_tech_d,
              'what_is_in_the_box': what_is_in_the_box}

    response = render(request, 'shop/product_desc.html', params)

    # For recent viewed items
    # response.delete_cookie('recentitems')
    if not request.COOKIES.get('recentitems'):
        arr = []
        arr.append(product.product_id)
    else:
        arr = eval(request.COOKIES.get('recentitems'))
        arr.append(product.product_id)
    response.set_cookie('recentitems', str(arr))
    return response


# Cart page
def AddToCart(request, id):
    if request.method == 'GET':
        product = Product.objects.get(product_id=id)
        cartitem, is_added = Cart.objects.get_or_create(
            user=request.user, product=product, totalprice=product.product_price)
        messages.success(request, "Item Successfully Added To Cart")
        getCartItems(request)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removecartitem(request):
    if request.method == 'POST':
        id = request.POST['id']
        Cart.objects.filter(id=id).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    cartitems = Cart.objects.filter(user=request.user)
    params = {
        'cartitems': cartitems,
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
        try:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your Account has been successfully created.")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")
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
        try:
            product = Product.objects.get(product_id=product_id)

            review = Review.objects.create(user=request.user,
                                        product=product, name=username, heading=heading, rating=rating, body=body)

            review.save()
            for img in imgs:
                ReviewImage.objects.create(
                    image=img, review=review, product=product)
            messages.success(request, "Review Successfully Submitted")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def liked(request):
    if request.method == 'POST':
        reviewId = request.POST['reviewId']
        review = Review.objects.get(id=reviewId)
        item,is_added=Like.objects.get_or_create(user=request.user, content_object=review)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def disliked(request):
    if request.method == 'POST':
        reviewId = request.POST['reviewId']
        review = Review.objects.get(id=reviewId)
        item,is_added=Dislike.objects.get_or_create(user=request.user,content_object=review)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def category(request, string):
    cat = Category.objects.get(name=string)
    products = Product.objects.filter(Category_id=cat.id)
    params = {'products': products}
    return render(request, 'shop/category_desc.html', params)


def subcategory(request, string):
    scat = SubCategory.objects.get(name=string)
    products = Product.objects.filter(Sub_Category=scat)
    return render(request, 'shop/category_desc.html', {'products': products})





def payment(request):
    addresses = Address.objects.filter(
        user_id=request.user).order_by('-default_address')

    if request.COOKIES.get('cartitems'):
        cart_items = eval(request.COOKIES.get('cartitems'))

    print(cart_items)

    ids = [int(x[0]) for x in cart_items]

    qs = list(Product.objects.filter(product_id__in=ids).values())
    for j in cart_items:
        for i in range(len(qs)):
            if qs[i]['product_id'] == int(j[0]):
                qs[i]['quantity'] = int(j[1])
                qs[i]['total_price'] = int(j[1])*qs[i]['product_price']

    sub_total = 0
    total = 0
    shipping_charges = 0
    for i in qs:
        sub_total += i['product_price']*i['quantity']
        total += i['product_price']*i['quantity']+i['product_shipping_charges']
        shipping_charges += i['product_shipping_charges']

    if sub_total > 1500:
        shipping_charges = 0
        total = sub_total

    params = {'products': qs,
              'total': total,
              'sub_total': sub_total,
              'shipping_charges': shipping_charges,
              'addresses': addresses,
              }
    if request.method == "POST":
        address_id = request.POST['address_id']
        card_holder_name = request.POST['cardholdername']
        card_holder_number = request.POST['cardholdernumber']
        expiry_date = request.POST["expiry_date"]
        ccv_number = request.POST["ccv_number"]
        address = Address.objects.get(id=address_id)
        print(address_id, card_holder_name,
              card_holder_number, ccv_number, expiry_date)
        for prd in qs:
            product = Product.objects.get(product_id=prd['product_id'])
            order = Order.objects.create(user=request.user, product=product,
                                         quantity=prd['quantity'], address=address, final_price=prd['total_price'])
            order.save()

    return render(request, 'shop/paymentGateway.html', params)


def getMyRecentSearchItems(request):
    if request.method == 'GET':
        return JsonResponse("ewrdg", safe=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# An Fetch request to update the cart items every time 
def getCartItems(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            items = Cart.objects.filter(user_id=request.user.id)
            data = {'num': len(items)}
            return JsonResponse(data, safe=False)
