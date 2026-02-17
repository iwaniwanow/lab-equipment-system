from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/update/', views.equipment_update, name='equipment_update'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
]
