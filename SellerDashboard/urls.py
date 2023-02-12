from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.site.site_header = 'MBCART'
admin.site.index_title = 'Welcome User'
urlpatterns = [
    path('',views.dashboard,name="dashboard"),
]
