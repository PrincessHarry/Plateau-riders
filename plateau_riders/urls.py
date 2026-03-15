from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.booking.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('routes/', include('apps.routes.urls')),
    path('waybill/', include('apps.waybill.urls')),
    path('buses/', include('apps.buses.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
