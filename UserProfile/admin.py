from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Address)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('address','product','quantity', 'order_date')
    list_filter = ('order_date',)
    search_fields = ('address', 'product')
    
    class Meta:
        model = Order
        
# admin.site.register(User)
admin.site.register(Notification)