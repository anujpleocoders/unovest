from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    # fake url for admin for identify fake login attempt on admin site
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/', include('unovestAdmin.urls')),
    path('superuser/', admin.site.urls),
]
