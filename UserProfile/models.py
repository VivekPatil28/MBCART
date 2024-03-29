from shop import models as model
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(model.User, on_delete=models.SET_DEFAULT, default=None)
    full_name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=20)
    alternate_phone_number = models.CharField(max_length=20)
    pincode = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    house_no = models.CharField(max_length=200)
    area = models.CharField(max_length=500)
    home_work_address = models.BooleanField(default=True)
    # true means home and false means work
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return str(self.full_name)


class Order(models.Model):
    product = models.ForeignKey(
        model.Product, on_delete=models.SET_DEFAULT, default=None
    )
    address = models.ForeignKey(Address, on_delete=models.SET_DEFAULT, default=None)
    user = models.ForeignKey(
        model.User,
        on_delete=models.SET_DEFAULT,
        default=None,
    )
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateField(null=True,blank=True)
    outfordelivery = models.BooleanField(default=False)
    outfordelivery_date = models.DateField(null=True,blank=True)
    delivered = models.BooleanField(default=False)
    delivered_date = models.DateField(null=True,blank=True)
    final_price = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=150, null=False)
    order_id = models.CharField(max_length=150,  null=False)
    signature = models.CharField(max_length=150, null=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)
