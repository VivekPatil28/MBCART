from shop import models as model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        related_name="orders",
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

@receiver(post_save, sender=Order)
def do_something(sender, instance,created, **kwargs):
    if instance.canceled:
        n=Notification.objects.create(user=instance.user,notification=f"Your Product <a href='/profile/myorders'>{' '.join(instance.product.product_name.split(' ')[:5])+'...'}</a> has been Cancelled")
        n.save()
    elif instance.delivered:                                                               
        n=Notification.objects.create(user=instance.user,notification=f"Your Product <a href='/profile/myorders'>{' '.join(instance.product.product_name.split(' ')[:5])+'...'}</a> has been Delivered")
        n.save()
    elif instance.outfordelivery:
        print(instance.outfordelivery)
        n=Notification.objects.create(user=instance.user,notification=f"Your Product <a href='/profile/myorders'>{' '.join(instance.product.product_name.split(' ')[:5])+'...'}</a> has been Out For Delievery")
        n.save()
    elif instance.shipped:
        n=Notification.objects.create(user=instance.user,notification=f"Your Product <a href='/profile/myorders'>{' '.join(instance.product.product_name.split(' ')[:5])+'...'}</a> has been shipped Now")
        n.save()
    elif created:
        n=Notification.objects.create(user=instance.user,notification=f"Your Product <a href='/profile/myorders'>{ ' '.join(instance.product.product_name.split(' ')[:5])+'...' }</a> has been Ordered")
        n.save()

from datetime import datetime
class Notification(models.Model):
    user=models.ForeignKey(model.User,on_delete=models.CASCADE)
    notification=models.CharField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)
    def how_old(self):
        date = self.created_at.replace(tzinfo=None)
        if (datetime.now()-date).total_seconds() < 3600:
            return f"{int((datetime.now() - date).total_seconds() // 60)}m"
        elif (datetime.now() - date).days < 1:
            return f'{int((datetime.now() - date).total_seconds()//3600)}h'
        elif (datetime.now() - date).days < 7:
            return f'{int((datetime.now() - date).total_seconds()//84600)}d'
        elif (datetime.now() - date).days < 30:
            return (datetime.now() - date).days//7
        elif (datetime.now() - date).days < 365:
            return (datetime.now() - date).days//30.5
        else:
            return (datetime.now() - date).days//365
        
    def __str__(self) -> str:
        return self.notification

