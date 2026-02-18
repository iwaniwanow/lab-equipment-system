from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('equipment.urls')),
    path('', include('inspections.urls')),
    path('', include('maintenance.urls')),
]

# Custom error handlers
handler404 = 'equipment.views.custom_404'

