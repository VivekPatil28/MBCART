from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name="ShopHome"),
    path('about', views.about, name="About"),
    path('cart', views.cart, name="Cart"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('submitReview', views.submitReview, name="submitReview"),
    path('searchResult', views.search, name="search"),
    path('product/<int:id>', views.product_desc, name="product_desc"),
    path('AddToCart/<int:id>', views.AddToCart, name="addtocart"),
    path('liked', views.liked, name="liked"),
    path('disliked', views.disliked, name="disliked"),
    path('removecartitem', views.removecartitem, name="removecartitem"),
    path('category/<str:string>', views.category, name="category_desc"),
    path('subcategory/<str:string>', views.subcategory, name="sub_cat_desc"),
    path('getCartItems', views.getCartItems, name="getCartItems"),
    path('payment', views.payment, name="payment"),
    path('getMyRecentSearchItems', views.getMyRecentSearchItems,name="getMyRecentSearchItems"),
    path('search', views.search_product,name="search_product"),
    path('FAQ', views.faq,name="faq"),
    path('compare',views.compareview,name="Compare"),
    path('add_compare_item',views.add_compare_item,name="add_compare_item"),
    path('similar_products',views.show_similar_products,name='similar_products'),
    path('notifications_viewed',views.notifications_viewed,name='notifications_viewed'),
    path('chatbot/',views.chatbot_response,name='chatbot_response'),
]