import imp
from django.contrib import admin

# Register your models here.
from .models import Contact, Coursal, Product
admin.site.register(Product)
admin.site.register(Coursal)
admin.site.register(Contact)