from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    path('maintenance/<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),

    path('maintenance-types/', views.maintenance_type_list, name='maintenance_type_list'),
    path('maintenance-types/<int:pk>/', views.maintenance_type_detail, name='maintenance_type_detail'),
    path('maintenance-types/create/', views.maintenance_type_create, name='maintenance_type_create'),
    path('maintenance-types/<int:pk>/update/', views.maintenance_type_update, name='maintenance_type_update'),
    path('maintenance-types/<int:pk>/delete/', views.maintenance_type_delete, name='maintenance_type_delete'),
]
