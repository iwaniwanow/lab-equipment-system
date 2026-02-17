from django.urls import path
from . import views

urlpatterns = [
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    path('maintenance/<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    path('maintenance/<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),
]
