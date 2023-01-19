from xml.etree.ElementInclude import default_loader
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='shop/Category_thumbnail', default='')

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
    product_name = models.TextField()
    product_desc = models.TextField()
    product_techinical_details=models.TextField(default=" ")
    what_is_in_the_box = models.TextField()
    product_price = models.IntegerField()
    image = models.ImageField(upload_to='shop/thumbnail_image', default='')
    product_rating = models.FloatField()
    product_shipping_charges = models.IntegerField(default=0)
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
    image = models.ImageField(upload_to='shop/DescImages', default="shop/placeholder.png")

    def __str__(self):
        return self.product.product_name


# coursal images model

class Coursal(models.Model):
    coursal_id = models.AutoField(primary_key=True)
    coursal_image = models.ImageField(
        upload_to='shop/coursal_images', default="")
    image_url=models.CharField(max_length=1000)

    def __str__(self):
        return "Coursal_Image "+str(self.coursal_id)

# Contact model


class Contact(models.Model):
    message_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phoneNumber = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity=models.PositiveIntegerField(default=1)
    totalprice=models.IntegerField()
    
    def __str__(self):
        return str(self.user)
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name='comments')
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=500)
    heading = models.CharField(max_length=1000)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'comment by {} on {}'.format(self.name, self.product)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_object = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.user)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_object = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)
    
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/Reviewimages')

    def __str__(self):
        return str(self.id)
    
    
class StaticImage(models.Model):
    cat=models.CharField(default="",max_length=500)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/static')
    
    def __str__(self):
        return str(self.image)