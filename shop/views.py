from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from UserProfile.models import Address
from UserProfile.models import Order
from UserProfile.models import Notification
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from fuzzysearch import find_near_matches
from django.contrib import messages
from redmail import gmail

from shop.keys import gmailkey as gk
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect

from xhtml2pdf import pisa
import os


# Home Page
def index(request):
    products = Product.objects.all()
    coursal = Coursal.objects.all()
    productimg = ProductImages.objects.all()
    category = Category.objects.all()
    latest_laptops = (
        Product.objects.filter(Category_id=5).order_by("-product_publish_date").values()
    )
    latest_mobiles = (
        Product.objects.filter(Category_id=1).order_by("-product_publish_date").values()
    )
    latest_headphones = (
        Product.objects.filter(Category_id=2).order_by("-product_publish_date").values()
    )
    cart = ""
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
    params = {
        "product": products,
        "coursal": coursal,
        "thumbnail": productimg,
        "cart": cart,
        "category": category,
        "latest_laptops": latest_laptops,
        "latest_mobiles": latest_mobiles,
        "latest_headphones": latest_headphones,
    }

    if request.COOKIES.get("recentitems"):
        recent_items = eval(request.COOKIES.get("recentitems"))
        params["recent_items"] = recent_items[3::-1]

    if request.COOKIES.get("recentsearch"):
        recent_search = eval(request.COOKIES.get("recentsearch"))
        params["recent_search"] = recent_search[3::-1]

    return render(request, "shop/index.html", params)


#  Search functionality using fuzzysearch module
# tries to match the patterns and return response
def search(request):  
    query = request.GET.get("search", "")
    query = query.strip()
    ids = set()
    query = query.lower().replace(" ", "")

    if query == "":
        return index(request)

    category = Category.objects.all()
    subcat = SubCategory.objects.all()
    products = Product.objects.all()
    for cat in category:
        s = find_near_matches(query, cat.name.lower(), max_l_dist=1)
        if s != []:
            product = Product.objects.filter(Category_id=cat.id)
            for i in product:
                ids.add(i.product_id)

    for sc in subcat:
        s = find_near_matches(query, sc.name.lower(), max_l_dist=1)
        if s != []:
            product = Product.objects.filter(Sub_Category_id=sc.id)
            for i in product:
                ids.add(i.product_id)

    if not ids:
        for product in products:
            split_names = product.product_name.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                if s != []:
                    ids.add(product.product_id)

        for product in products:
            split_names = product.product_desc.split(" ")
            split_names = split_names
            for word in split_names:
                s = find_near_matches(query, word.lower(), max_l_dist=1)
                if s != []:
                    ids.add(product.product_id)

    # Only the result objects
    qs = Product.objects.none()
    for i in ids:
        qs = qs | Product.objects.filter(product_id=i)

    params = {"query": query, "ids": ids, "product": qs}
    response = render(request, "shop/searchResult.html", params)
    # For recent search items
    # response.delete_cookie('recentsearch')
    if not request.COOKIES.get("recentsearch"):
        response.set_cookie("recentsearch", str(list(ids)))
    else:
        arr = eval(request.COOKIES.get("recentsearch"))
        for i in ids:
            if i not in arr:
                arr.append(i)
        response.set_cookie("recentsearch", str(arr))

    return response


def compareview(request):
    ids = eval(request.COOKIES.get("CompareValues"))
    prods = Product.objects.filter(product_id__in=ids)

    samecategory = Product.objects.filter(Category_id=prods.first().Category_id)
    params={'compareproductlist':prods,
            'sc':samecategory,}
    return render(request,'shop/compare.html',params)

def add_compare_item(request):
    item_id = request.GET.get('item')
    ids = eval(request.COOKIES.get("CompareValues"))
    prods = Product.objects.filter(product_id__in=ids)
    category = prods.first().Category
    for i in prods:
        if i.Category!= category:
            return JsonResponse({"is_valid": False})
    return JsonResponse({"is_valid":True})

# About section page
def about(request):
    return render(request, "shop/about.html")


# profuct Description page
def product_desc(request, id):
    product = Product.objects.get(product_id=id)
    sub_cat = SubCategory.objects.get(id=product.Sub_Category_id)
    if not request.user:
        my_orders=Order.objects.filter(user=request.user).values_list(flat=True)
    my_orders=""
    samecategory = (Product.objects.filter(Category_id=product.Category_id)).exclude(
        product_id=id
    )
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

    total_ratings = sum(r.rating for r in Reviews)
    product_rating = total_ratings / len(Reviews) if len(Reviews) > 0 else 0
    product.product_rating = product_rating
    product.save(force_update=True)
    
    
    if request.COOKIES.get("CompareValues"):
        compare_items = eval(request.COOKIES.get("CompareValues"))
        prods = Product.objects.filter(product_id__in=compare_items)
    else:
        prods=[]
    
    params = {
        "compare_items":prods,
        "product": product,
        "sc": samecategory,
        "user_review": user_review,
        "sub_cat": sub_cat,
        "is_added_to_cart": is_added_to_cart,
        "aboutthisitem": desc,
        "what_is_in_the_box": what_is_in_the_box,
        "my_orders":my_orders,
    }

    response = render(request, "shop/product_desc.html", params)

    # For recent viewed items
    # response.delete_cookie('recentitems')
    arr = (
        eval(request.COOKIES.get("recentitems"))
        if request.COOKIES.get("recentitems")
        else []
    )
    arr.append(product.product_id)
    response.set_cookie("recentitems", str(arr))
    return response


# Cart page
def AddToCart(request, id):
    if request.method == "GET":
        product = Product.objects.get(product_id=id)
        cartitem, is_added = Cart.objects.get_or_create(
            user=request.user, product=product, totalprice=product.product_price
        )
        messages.success(request, "Item Successfully Added To Cart")
        getCartItems(request)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# Fetch request to add an item to cart

# def AddToCart(request, id):
#     if request.method == "GET":
#         product = Product.objects.get(product_id=id)
#         cartitem, is_added = Cart.objects.get_or_create(
#             user=request.user, product=product, totalprice=product.product_price
#         )
#         messages.success(request, "Item Successfully Added To Cart")
#         getCartItems(request)
#         return JsonResponse("True", safe=False)


def removecartitem(request):
    if request.method == "POST":
        item = request.POST["id"]
        Cart.objects.filter(id=item).delete()
        messages.error(request, "Item Successfully Removed From Cart")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart(request):
    cartitems = Cart.objects.filter(user=request.user)
    params = {
        "cartitems": cartitems,
    }
    return render(request, "shop/cart.html", params)


def signup(request):
    if request.method == "POST":
        # we can also write like this
        # username=request.POST['username']
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username):
            messages.error(request, "The Username has already been taken !")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        try:
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your Account has been successfully created.")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# Sign in and Signout functions to sign in or out


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")

        else:
            messages.error(request, "Invalid Credentials")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def signout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return HttpResponseRedirect("/")


def submitReview(request):
    if request.method == "POST":
        imgs = request.FILES.getlist("imgs[]")
        username = request.POST["username"]
        product_id = request.POST["product"]
        rating = request.POST["rating"]
        heading = request.POST["heading"]
        body = request.POST["body"]
        try:
            product = Product.objects.get(product_id=product_id)
            review = Review.objects.create(
                user=request.user,
                product=product,
                name=username,
                heading=heading,
                rating=rating,
                body=body,
            )

            review.save()
            for img in imgs:
                ReviewImage.objects.create(image=img,review=review)
            messages.success(request, "Review Successfully Submitted")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def liked(request):
    if request.method == "POST":
        reviewId = request.POST["reviewId"]
        review = Review.objects.get(id=reviewId)
        if item := Dislike.objects.filter(user=request.user, content_object=review):
            item.delete()
        item, is_added = Like.objects.get_or_create(
            user=request.user, content_object=review
        )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def disliked(request):
    if request.method == "POST":
        reviewId = request.POST["reviewId"]
        review = Review.objects.get(id=reviewId)
        if item := Like.objects.filter(user=request.user, content_object=review):
            item.delete()
        item, is_added = Dislike.objects.get_or_create(
            user=request.user, content_object=review
        )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def category(request, string):
    cat = Category.objects.get(name=string)
    products = Product.objects.filter(Category_id=cat.id)
    params = {"products": products}
    return render(request, "shop/category_desc.html", params)


def subcategory(request, string):
    scat = SubCategory.objects.get(name=string)
    products = Product.objects.filter(Sub_Category=scat)
    return render(request, "shop/category_desc.html", {"products": products})


def payment(request):
    addresses = Address.objects.filter(user_id=request.user).order_by(
        "-default_address"
    )
    if request.COOKIES.get("cartitems"):
        cart_items = eval(request.COOKIES.get("cartitems"))
    else:
        return HttpResponseRedirect("/")

    ids = [int(x[0]) for x in cart_items]
    
    qs = list(Product.objects.filter(product_id__in=ids).values())

    for j in cart_items:
        for q in qs:
            if q["product_id"] == int(j[0]):
                q["quantity"] = int(j[1])
                q["total_price"] = int(j[1]) * q["product_price"]

    sub_total = 0
    total = 0
    shipping_charges = 0
    for i in qs:
        sub_total += i["product_price"] * i["quantity"]
        total += i["product_price"] * i["quantity"] + i["product_shipping_charges"]
        shipping_charges += i["product_shipping_charges"]

    if sub_total > 1500:
        shipping_charges = 0
        total = sub_total

    params = {
        "products": qs,
        "total": total,
        "sub_total": sub_total,
        "shipping_charges": shipping_charges,
        "addresses": addresses,
    }

    import razorpay
    from shop.keys import keys as k

    client = razorpay.Client(auth=(k.key1, k.key2))
    payment = client.order.create(
        {"amount": total * 100, "currency": "INR", "payment_capture": 1}
    )
    params["payment"] = payment

    if request.method == "POST":
        address_id = request.POST["address_id"]
        razorpay_payment_id = request.POST["razorpay_payment_id"]
        razorpay_order_id = request.POST["razorpay_order_id"]
        razorpay_signature = request.POST["razorpay_signature"]

        address = Address.objects.get(id=address_id)
        product_list_string = ""
        for prd in qs:
            product = Product.objects.get(product_id=prd["product_id"])
            product_list_string += f"{product.product_name}, "
            order = Order.objects.create(
                user=request.user,
                product=product,
                quantity=prd["quantity"],
                address=address,
                final_price=total,
                payment_id=razorpay_payment_id,
                order_id=razorpay_order_id,
                signature=razorpay_signature,
            )
            order.save()

        template = f"""<!DOCTYPE html>
                    <html>
                    <head>
                    <title></title>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" />
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.bundle.min.js" />
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js" />
                    <style type="text/css">

                    body, table, td, a {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
                    table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
                    img {{ -ms-interpolation-mode: bicubic; }}

                    img {{ border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }}
                    table {{ border-collapse: collapse !important; }}
                    body {{ height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }}


                    a[x-apple-data-detectors] {{
                        color: inherit !important;
                        text-decoration: none !important;
                        font-size: inherit !important;
                        font-family: inherit !important;
                        font-weight: inherit !important;
                        line-height: inherit !important;
                    }}
                    div[style*="margin: 16px 0;"] {{ margin: 0 !important; }}
                    </style>
                    <body style="margin: 0 !important; padding: 0 !important; background-color: #eeeeee;" bgcolor="#eeeeee">


                    <div style="display: none; font-size: 1px; color: #fefefe; line-height: 1px; font-family: Open Sans, Helvetica, Arial, sans-serif; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
                    For what reason would it be advisable for me to think about business content? That might be little bit risky to have crew member like them. 
                    </div>

                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td align="center" style="background-color: #eeeeee;" bgcolor="#eeeeee">
                            
                            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                                <tr>
                                    <td align="center" valign="top" style="font-size:0; padding: 35px;" bgcolor="#F44336">
                                
                                    <div style="display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;">
                                        <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                                            <tr>
                                                <td align="left" valign="top" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 36px; font-weight: 800; line-height: 48px;" class="mobile-center">
                                                    <h1 style="font-size: 36px; font-weight: 800; margin: 0; color: #ffffff;text-align:center;">MBCART</h1>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                    
                                    <div style="display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;" class="mobile-hide">
                                        <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                                            <tr>
                                                <td align="right" valign="top" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; line-height: 48px;">
                                                    <table cellspacing="0" cellpadding="0" border="0" align="right">
                                                        <tr>
                                                            <td style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400;">
                                                                <p style="font-size: 18px; font-weight: 400; margin: 0; color: #ffffff;"><a href="#" target="_blank" style="color: #ffffff; text-decoration: none;">Shop &nbsp;</a></p>
                                                            </td>
                                                            <td style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 24px;">
                                                                <a href="#" target="_blank" style="color: #ffffff; text-decoration: none;"><img src="https://img.icons8.com/color/48/000000/small-business.png" width="27" height="23" style="display: block; border: 0px;"/></a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding: 35px 35px 20px 35px; background-color: #ffffff;" bgcolor="#ffffff">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                                        <tr>
                                            <td align="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 25px;">
                                                <img src="https://img.icons8.com/carbon-copy/100/000000/checked-checkbox.png" width="125" height="120" style="display: block; border: 0px;" /><br>
                                                <h2 style="font-size: 30px; font-weight: 800; line-height: 36px; color: #333333; margin: 0;">
                                                    Thank You For Your Order!
                                                </h2>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 10px;">
                                                <p style="font-size: 16px; font-weight: 400; line-height: 24px; color: #777777;">
                                                    Thanks for shopping! Your order <b>{product_list_string}</b>hasen't shipped yet, but we'll send an email when it does.
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="padding-top: 20px;">
                                                <table cellspacing="0" cellpadding="0" border="0" width="100%">
                                                    <tr>
                                                        <td width="75%" align="left" bgcolor="#eeeeee" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;">
                                                            Order Confirmation #
                                                        </td>
                                                        <td width="25%" align="left" bgcolor="#eeeeee" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;">
                                                            {razorpay_order_id}
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 15px 10px 5px 10px;">
                                                            Purchased Item ({len(qs)})
                                                        </td>
                                                        <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 15px 10px 5px 10px;">
                                                            ₹{sub_total}
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 5px 10px;">
                                                            Shipping + Handling
                                                        </td>
                                                        <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 5px 10px;">
                                                            ₹{shipping_charges}
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="padding-top: 20px;">
                                                <table cellspacing="0" cellpadding="0" border="0" width="100%">
                                                    <tr>
                                                        <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px; border-top: 3px solid #eeeeee; border-bottom: 3px solid #eeeeee;">
                                                            TOTAL
                                                        </td>
                                                        <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px; border-top: 3px solid #eeeeee; border-bottom: 3px solid #eeeeee;">
                                                            ₹{total}
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" height="100%" valign="top" width="100%" style="padding: 0 35px 35px 35px; background-color: #ffffff;" bgcolor="#ffffff">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px;">
                                        <tr>
                                            <td align="center" valign="top" style="font-size:0;">
                                                <div style="display:inline-block; max-width:50%; min-width:240px; vertical-align:top; width:100%;">

                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                                                        <tr>
                                                            <td align="left" valign="top" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px;">
                                                                <p style="font-weight: 800;">Delivery Address</p>
                                                                <p>{address.full_name} <br> {address.house_no} {address.area} {address.city} <br>{address.state} {address.pincode}</p>

                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                                <div style="display:inline-block; max-width:50%; min-width:240px; vertical-align:top; width:100%;">
                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                                                        <tr>
                                                            <td align="left" valign="top" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px;">
                                                                <p style="font-weight: 800;">Estimated Delivery Date</p>
                                                                <p>January 1st, 2016</p>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style=" padding: 35px; background-color: #ff7361;" bgcolor="#1b9ba3">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                                        <tr>
                                            <td align="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 25px;">
                                                <h2 style="font-size: 24px; font-weight: 800; line-height: 30px; color: #ffffff; margin: 0;">
                                                    Get 30% off your next order.
                                                </h2>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 25px 0 15px 0;">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    <tr>
                                                        <td align="center" style="border-radius: 5px;" bgcolor="#66b3b7">
                                                        <a href="#" target="_blank" style="font-size: 18px; font-family: Open Sans, Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; border-radius: 5px; background-color: #F44336; padding: 15px 30px; border: 1px solid #F44336; display: block;">Shop Again</a>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding: 35px; background-color: #ffffff;" bgcolor="#ffffff">
                                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 24px;">
                                                <p style="font-size: 14px; font-weight: 400; line-height: 20px; color: #777777;">
                                                Thank you for shopping with US.
                                                <b><a href="">MBCART</a></b>
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                    </td>
                                </tr>
                            </table>
                            </td>
                        </tr>
                    </table>
                        
                    </body>
                    </html>
                    """

        
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.conf import settings
        from django.http import HttpResponse
        
        subject = 'Welcome to our site!'
        to_email = request.user.email
        print(request.user.email)
        from_email = settings.DEFAULT_FROM_EMAIL

        # Context data for the email template
        context = {
            'name': 'John Doe',  # Pass dynamic data for personalization
        }

        # Render the HTML template
        html_message = render_to_string('UserProfile/invoice.html', context)

        # Send the email
        send_mail(
            subject,               # Subject of the email
            '',                    # Plain text message (leave empty if sending HTML only)
            from_email,            # From email address
            [to_email],            # Recipient email list
            html_message=html_message,  # The HTML email content
        )
        
        # template = get_template('UserProfile/invoice.html')
        # html = template.render({'request': request, 'order': order})

        # # Generate the PDF file
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="invoice-{order.product.product_name[:40]}....pdf"'
        # pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

        # # Check if PDF generation was successful
        # if pisa_status.err:
        #     return HttpResponse('Failed to generate PDF', status=500)

        # # Create an EmailMessage instance
        # email = EmailMessage(
        #     "Order Confirmation, Your Order has been Successfully Placed",
        #     "Hi, Customer",
        #     gk.username,
        #     [request.user.email],
        #     html_message=template
        # )
        
        # email.attach(f'invoice-{order.product.product_name[:40]}....pdf', response.getvalue(), 'application/pdf')
        # email.send()

        return render(request, "shop/success.html", params)
    return render(request, "shop/paymentGateway.html", params)

def link_callback(uri, rel):
    from django.conf import settings
    from django.contrib.staticfiles import finders
    if result := finders.find(uri):
        return result
    else:
        return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

def getMyRecentSearchItems(request):
    if request.method == "GET":
        return JsonResponse("ewrdg", safe=False)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
def faq(request):
    return render(request,'shop/FAQ.html')

from django.core import serializers
# An Fetch request to update the cart items every time
def getCartItems(request):
    if request.user.is_authenticated and request.method == "GET":
        items = Cart.objects.filter(user_id=request.user.id)
        notifications=Notification.objects.filter(user_id=request.user.id,is_read=False).order_by("-created_at")
        ns=serializers.serialize('json', notifications)
        data = {"num": len(items),"notifications":ns}
        return JsonResponse(data, safe=False)
    return JsonResponse("", safe=False)

def notifications_viewed(request):
    if request.user.is_authenticated and request.method == "GET":
        notifications=Notification.objects.filter(user_id=request.user.id,is_read=False)
        for i in notifications:
            i.is_read=True
            i.save()
    return JsonResponse("", safe=False)

def search_product(request):
    if query := request.GET.get("value"):
        products = Product.objects.filter(
            product_name__icontains=query, product_desc__icontains=query
        )
        payload = [p.product_name for p in products]
    return JsonResponse({"data": payload})


def show_similar_products(request):
    if request.method=='POST':
        prod_id = request.POST['product_id']
        product= Product.objects.get(product_id=prod_id)
        samecategory = (Product.objects.filter(Category_id=product.Category_id)).exclude(product_id=prod_id)
        params={'products':samecategory,}
        return render(request,'shop/similar_products.html',params)
    
#chatbot Integration
from django.http import JsonResponse
from .chatbot.engine import get_bot_response

def chatbot_response(request):
    if request.user.is_authenticated:
        message = request.GET.get("message", "")
        product_id = request.GET.get("product", "")
        if product_id:
            product = Product.objects.get(product_id=product_id)
        else:
            product=None
        print(product)
        reply = get_bot_response(message,request,product)
    else: 
        reply = "Login for Chatbot Usage"
    return JsonResponse({'response': reply})
