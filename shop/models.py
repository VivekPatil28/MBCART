from email import message
from email.policy import default
from itertools import product
from operator import mod
from pyexpat import model
from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=100)
    product_desc=models.CharField(max_length=400)
    product_price=models.IntegerField()
    product_rating=models.FloatField()
    product_category = (
        ('Clothing','Clothing'),
        ('Electronics','Electronics'),
        ('Mobiles','Mobiles'),
        ('Laptop','Laptop'),
        ('Washing Machines','Washing Machines'),
        ('Computers','Computers'),
        ('Smart Watches','Smart Watches'),
        ('Toys','Toys'),
        ('Air Coolers','Air Coolers'),
        ('Headphones','Headphones'),
        ('Water Purifiers','Water Purifiers'),
        ('Trimmers','Trimmers'),
        ('Deodrants','Deodrants'),
        ('Anrivirous','Anrivirous'),
        ('Wallets','Wallets'),
        ('Fans','Fans'),
        ('Camera','Camera'),
        ('Deodorants','Deodorants'),
        ('College Bags','College Bags'),
        ('Laptop Bags','Laptop Bags'),
        ('Televisions','Televisions'),
    )
    category = models.CharField(max_length=100, choices=product_category)
    product_initial_price=models.IntegerField()
    product_publish_date=models.DateField()
    product_image=models.ImageField(upload_to='shop/images',default="")
    def __str__(self):
        return self.product_name
    
# coursal images model
class Coursal(models.Model):
    coursal_id=models.AutoField(primary_key=True)
    coursal_image=models.ImageField(upload_to='shop/coursal_images',default="")
    def __str__(self):
        return "Coursal_Image "+str(self.coursal_id)

# Contact model
class Contact(models.Model):
    message_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=50)
    phoneNumber=models.IntegerField()
    description=models.CharField(max_length=1000)
    def __str__(self):
        return self.name