from shop import models as model
from django.db import models

class Order(models.Model):
    product = models.ForeignKey(model.Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(model.User, on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(default=1)
    order_date = models.DateTimeField(
        auto_now_add=True)
    shipped=models.BooleanField(default=False)
    shipped_date=models.DateField()
    outfordelivery=models.BooleanField(default=False)
    outfordelivery_date=models.DateField(auto_now=False, auto_now_add=False)
    delivered=models.BooleanField(default=False)
    delivered_date=models.DateField(auto_now=False, auto_now_add=False,default='')    
    
    def __str__(self):
        return str(self.product)

    
class Address(models.Model):
    user= models.ForeignKey(model.User,on_delete=models.DO_NOTHING)
    full_name=models.CharField(max_length=500)
    phone_number=models.CharField(max_length=20)
    alternate_phone_number=models.CharField(max_length=20)
    pincode=models.CharField(max_length=20)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    house_no=models.CharField(max_length=200)
    area=models.CharField(max_length=500)
    home_work_address=models.BooleanField(default=True)
    # true means home and false means work
    
    def __str__(self):
        return str(self.user)
    
class User(model.User):
    mobile_no=models.CharField(max_length=50)
    # primary_address=models.OneToOneField(Address,on_delete=models.DO_NOTHING)
    
