# =========================
# eshop_project/urls.py (MAIN PROJECT URLS)
# =========================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('store.urls')),
    path('', include('accounts.urls')),
    path('', include('orders.urls')),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)