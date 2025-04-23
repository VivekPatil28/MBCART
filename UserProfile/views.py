from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from shop import models as model
from .models import *
from django.contrib import messages
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def profile(request):
    return render(request, "UserProfile/profile.html")


def address(request):
    address = Address.objects.filter(user=request.user)
    return render(request, "UserProfile/address.html", {"address": address})


def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by("-order_date")
    return render(request, "UserProfile/myorders.html", {"orders": orders})


def myreviews(request):
    reviews = model.Review.objects.filter(user=request.user)
    reviewImages = model.ReviewImage.objects.all()

    params = {"reviews": reviews, "ReviewImages": reviewImages}
    return render(request, "UserProfile/myreviews.html", params)


def addAddress(request):
    if request.method == "POST":
        name = request.POST["fullname"]
        number = request.POST["number"]
        alternateNumber = request.POST["alternateNumber"]
        state = request.POST["state"]
        city = request.POST["city"]
        pincode = request.POST["pincode"]
        houseno = request.POST["houseno"]
        area = request.POST["area"]
        homeaddress = request.POST.get("addresstype")

        address, is_added = Address.objects.get_or_create(
            user=request.user,
            full_name=name,
            phone_number=number,
            alternate_phone_number=alternateNumber,
            pincode=pincode,
            state=state,
            city=city,
            house_no=houseno,
            area=area,
            home_work_address=homeaddress,
        )
        if is_added:
            messages.success(request, "Address Successfully Added")
        else:
            messages.error(request, "Something went wrong try again later !")
        return redirect("/profile/myaddresses")

    return render(request, "UserProfile/addAddress.html")


def removeAddress(request, id):
    Address.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def contact(request):
    if request.method=='POST':
        try:
            name = request.POST.get("name", "")
            email = request.POST.get("email", "")
            phoneNumber = request.POST.get("phoneNumber", "")
            description = request.POST.get("description", "")
            contact = model.Contact(
                email=email, phoneNumber=phoneNumber, description=description, name=name
            )
            contact.save()
            messages.success(request, "Your response has been successfully submitted")
        except Exception as e:
            messages.error(request, "Something went wrong try again later !")

    return render(request, "UserProfile/contact.html")


def addProduct(request):
    return render(request, "UserProfile/addProduct.html")


def defaultAddressChanged(request):
    if request.method == "POST":
        addressId = request.POST["check"]
        user_address = Address.objects.filter(user=request.user)
        for add in user_address:
            add.default_address = False
            add.save()
        address = Address.objects.get(id=addressId)
        address.default_address = True
        address.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def cancelOrder(request,id):
    order = Order.objects.get(id=id)
    order.canceled = True
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

def downloadinvoice(request):
    # Load the HTML template
    if request.method == 'POST':
        id=request.POST['id']
        order= Order.objects.get(id=id)
        
        template = get_template('UserProfile/invoice.html')
        html = template.render({'request':request,'order': order})

        # Generate the PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice-{order.product.product_name[:40]}....pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
        #pdf downloading

        # Return the generated PDF file as a response
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF', status=500)
        return response
    return HttpResponseRedirect(request.META.get("HTTP_REFERER",'/'))

def link_callback(uri, rel):
    from django.conf import settings
    from django.contrib.staticfiles import finders
    if result := finders.find(uri):
        return result
    else:
        return os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    
