from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import на custom admin site
admin.site.site_header = "Система за лабораторно оборудване - Администрация"
admin.site.site_title = "Админ панел"
admin.site.index_title = "Табло за управление"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('', include('equipment.urls', namespace='equipment')),
    path('', include('inspections.urls', namespace='inspections')),
    path('', include('maintenance.urls', namespace='maintenance')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'equipment.views.custom_404'

