from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Coursal)
admin.site.register(Contact)
admin.site.register(StaticImage)

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Cart)

admin.site.register(ProductImages)
admin.site.register(ProductDescriptionImages)
admin.site.register(Like)
admin.site.register(Dislike)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImages


class ProductDescriptionImagesAdmin(admin.StackedInline):
    model = ProductDescriptionImages


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug', 'author', 'publish', 'status')

#     # to make a filter sidebar for filtering Posts
#     list_filter = ('status', 'created', 'publish', 'author')

#     # To Add a search field in the admin site

#     search_fields = ('title', 'body')

#     #to	prepopulate	the	slug field with the input of the title field
#     prepopulated_fields = {'slug': ('title',)}

#     raw_id_fields = ('author',)

#     # to navigate through a data hierarchy
#     date_hierarchy = 'publish'

#     # To add a ordering functionality on the admin site
#     ordering = ('status', 'publish')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_rating','product_price')
    list_filter = ('product_publish_date','product_price','product_rating')
    search_fields = ('product_name', 'product_desc')
    date_hierarchy = 'product_publish_date'
    ordering = ('product_rating','product_publish_date',)
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
