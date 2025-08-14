from django.contrib import admin  # You can keep this if needed elsewhere
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graziella.admin import admin_site  # ✅ Custom admin site

urlpatterns = [
    path('', include('graziella.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin_site.urls),  # ✅ Use Graziella-branded admin
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
