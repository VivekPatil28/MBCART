from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Coursal)
admin.site.register(Contact)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(StaticImage)
admin.site.register(Cart)

admin.site.register(ProductImages)
admin.site.register(ProductDescriptionImages)
admin.site.register(Like)
admin.site.register(Dislike)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImages


class ProductDescriptionImagesAdmin(admin.StackedInline):
    model = ProductDescriptionImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [ProductImageAdmin, ProductDescriptionImagesAdmin]

    class Meta:
        model = Product


class ReviewImageAdmin(admin.StackedInline):
    model = ReviewImage


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')

    inlines = [ReviewImageAdmin]

    class Meta:
        model = Review


@admin.register(ReviewImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
