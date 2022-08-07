from distutils.archive_util import make_zipfile
from distutils.command.upload import upload
from email.mime import image
from itertools import product
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    Sub_Category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
    Category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=400)
    product_desc = models.TextField(max_length=10000)
    product_price = models.IntegerField()
    image = models.ImageField(upload_to='shop/thumbnail_image', default='')
    product_rating = models.FloatField()
    product_initial_price = models.IntegerField()
    product_publish_date = models.DateField()

    def __str__(self):
        return self.product_name

# Product Images


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product.product_name


# Product Description Images
class ProductDescriptionImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/DescImages', default="")

    def __str__(self):
        return self.product.product_name


# coursal images model

class Coursal(models.Model):
    coursal_id = models.AutoField(primary_key=True)
    coursal_image = models.ImageField(
        upload_to='shop/coursal_images', default="")

    def __str__(self):
        return "Coursal_Image "+str(self.coursal_id)

# Contact model


class Contact(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phoneNumber = models.IntegerField()
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(default=1)
    totalprice=models.IntegerField()
    
    def __str__(self):
        return str(self.user)
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=500)
    heading = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'comment by {} on {}'.format(self.name, self.product)


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/Reviewimages')

    def __str__(self):
        return str(self.id)
    
    
class StaticImage(models.Model):
    cat=models.CharField(default="",max_length=500)
    image = models.ImageField(upload_to='shop/static')
    
    def __str__(self):
        return str(self.image)
       


