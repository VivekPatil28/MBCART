from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.site.site_header = 'MBCART'
admin.site.index_title = 'Welcome User'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('profile/',include("UserProfile.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)