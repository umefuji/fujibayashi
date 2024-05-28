

from django.contrib import admin
from django.urls import path, include
from shop import views as shop_views  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')), 
    path('accounts/', include('allauth.urls')),
    path('', shop_views.home, name='home'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)