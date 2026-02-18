from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Equipment URLs
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/update/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),

    # Manufacturer URLs
    path('manufacturers/', views.manufacturer_list, name='manufacturer_list'),
    path('manufacturers/<int:pk>/', views.manufacturer_detail, name='manufacturer_detail'),
    path('manufacturers/create/', views.manufacturer_create, name='manufacturer_create'),
    path('manufacturers/<int:pk>/update/', views.manufacturer_update, name='manufacturer_update'),
    path('manufacturers/<int:pk>/delete/', views.manufacturer_delete, name='manufacturer_delete'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
