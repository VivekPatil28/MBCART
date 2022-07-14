from operator import imod
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from .models import Coursal, Product,Contact

# Create your views here.
def index(request):
    products=Product.objects.all()
    coursal=Coursal.objects.all()
    params={'product':products,
            'coursal':coursal,
            }
    return render(request,'shop\index.html',params)

def search(request):
    query=request.GET.get('search','')
    query=query.strip()
    products=Product.objects.all()
    ids=set()
    query=query.lower()
    if (query==""):
        return index(request)    
    
    for product in products:
        if (product.category.lower()==query):
            ids.add(product.product_id)
    if (len(ids)==0):
        for product in products:
            split_names=product.product_name.split(" ")
            split_names=split_names
            for word in split_names:
                    if (word.lower()==query):
                        ids.add(product.product_id)
                    
    params={'query':query,
            'ids':ids,
            'product':products}
    return render(request,'shop/searchResult.html',params)

def about(request):
    
    return render(request,'shop/about.html')
def cart(request):
    return render(request,'shop/cart.html')

def contact(request):
    if (request.method=='POST'):
        name=request.POST.get('name','')
        email = request.POST.get('email','')
        phoneNumber = request.POST.get('phoneNumber','')
        description = request.POST.get('description','')
        contact=Contact(email=email,phoneNumber=phoneNumber,description=description,name=name)
        contact.save()
        contacts=Contact.objects.all()
        # params={'contact':contacts}
    return render(request,'shop/contact.html')

def product_desc(request,id):
    product=Product.objects.filter(product_id=id)[0]
    samecategory=Product.objects.filter(category=product.category)
    params = {'product': product, 'sc': samecategory}
    return render(request,'shop/product_desc.html',params)
    