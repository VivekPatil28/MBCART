from operator import imod
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Coursal, Product, Contact
from django.contrib.auth.models import User
from fuzzysearch import find_near_matches
# Create your views here.


# Home Page
def index(request):
    products = Product.objects.all()
    coursal = Coursal.objects.all()
    params = {'product': products,
              'coursal': coursal,
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

    for product in products:
        s = find_near_matches(query, product.category.lower(), max_l_dist=1)
        print(s)
        if (s != []):
            ids.add(product.product_id)
    if (len(ids) == 0):
        for product in products:
            split_names = product.product_name.split(" ")
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


# Cart
def cart(request):
    if (isAuthenticated(request)):
        return render(request, 'shop/cart.html')
    else:
        return render(request,'shop/login.html')

# to check the user was signuped or not
def isAuthenticated(request):
    pass

# signin response
def Authenticate(request):
    pass
        

# contact page
def contact(request):
    return render(request, 'shop/contact.html',{"success":'0'})


# to submit the user response
def submitform(request):
    if (request.method == 'POST'):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phoneNumber = request.POST.get('phoneNumber', '')
        description = request.POST.get('description', '')
        contact = Contact(email=email, phoneNumber=phoneNumber,description=description, name=name)
        contact.save()
        
        return render(request, 'shop/contact.html', {"success": '1'})


# profuct Description page
def product_desc(request, id):
    product = Product.objects.filter(product_id=id)[0]
    samecategory = Product.objects.filter(category=product.category)
    params = {'product': product, 'sc': samecategory}
    return render(request, 'shop/product_desc.html', params)


# Cart page
def AddToCart(request, id):
    return index(request)
