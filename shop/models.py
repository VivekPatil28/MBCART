from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="Category_thumbnail", default="")

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    Category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    Sub_Category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
    product_name = models.TextField()
    product_desc = models.TextField()
    product_techinical_details = models.TextField(default=" ")
    what_is_in_the_box = models.TextField()
    product_price = models.IntegerField()
    image = models.ImageField(upload_to="thumbnail_image", default="")
    product_rating = models.FloatField()
    product_shipping_charges = models.IntegerField(default=0)
    product_initial_price = models.IntegerField()
    product_publish_date = models.DateField()

    def __str__(self):
        return self.product_name


# Product Images
class StaticImage(models.Model):
    cat=models.CharField(default="", max_length=500) 
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static')
    def _str_(self):
        return str(self.image)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", default="")

    def __str__(self):
        return self.product.product_name


# Product Description Images
class ProductDescriptionImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="DescImages", default="")

    def __str__(self):
        return self.product.product_name


# coursal images model

class Coursal(models.Model):
    coursal_id = models.AutoField(primary_key=True)
    coursal_image = models.ImageField(upload_to="coursal_images", default="")
    image_url = models.CharField(max_length=1000)

    def __str__(self):
        return "Coursal_Image " + str(self.coursal_id)


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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=1)
    totalprice = models.IntegerField()

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=500)
    heading = models.CharField(max_length=1000)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return "comment by {} on {}".format(self.name, self.product)


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
    image = models.ImageField(upload_to="Reviewimages")

    def __str__(self):
        return str(self.id)


# class Color(models.Model):
#     name = models.CharField(max_length=28)
#     code = models.CharField(max_length=20, blank=True, null=True)
#     def __str__(self) -> str:
#             return self.name
#     def color_tag(self):
#         if self.code is not None:
#             return mark_safe("f<p style='background-color:{self.code}'>Color</p>")
#         else:
#             return ""

# class Size(models.Model):
#     name = models.CharField(max_length=20)
#     code = models.CharField(max_length=10, blank=True, null=True)

#     def __str__(self) -> str:
#         return self.name


# class Variant(models.Model):
#     title = models.CharField(max_length=150, blank=True, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color=models.ForeignKey(Color,on_delete=models.CASCADE,blank=True,null=True)
#     size=models.ForeignKey(Size,on_delete=models.CASCADE,blank=True,null=True)
#     image_id = models.ForeignKey(ProductImages,on_delete=models.CASCADE)
#     quantity=models.IntegerField(default=1)
#     price =models.FloatField(default=0)

#     def __str__(self) -> str:
#         return self.title
#     def image(self):
#         img=Image.objects.get(id=self.image_id)
#         if img.id is not None:
#             var=img.image.url
#         else:
#             var=''
#         return var

#     def image_tag(self):
#         img =Image.objects.get(id=self.image_id)
#         if img.id is not None:
#             return mark_safe(f"<img src='{img.image_url}' height='50' />")
#         else:
#             return ''
