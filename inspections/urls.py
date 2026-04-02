from django.urls import path
from . import views

app_name = 'inspections'

urlpatterns = [
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspections/<int:pk>/', views.inspection_detail, name='inspection_detail'),
    path('inspections/create/', views.inspection_create, name='inspection_create'),
    path('inspections/<int:pk>/update/', views.inspection_update, name='inspection_update'),
    path('inspections/<int:pk>/delete/', views.inspection_delete, name='inspection_delete'),

    path('inspection-types/', views.inspection_type_list, name='inspection_type_list'),
    path('inspection-types/<int:pk>/', views.inspection_type_detail, name='inspection_type_detail'),
    path('inspection-types/create/', views.inspection_type_create, name='inspection_type_create'),
    path('inspection-types/<int:pk>/update/', views.inspection_type_update, name='inspection_type_update'),
    path('inspection-types/<int:pk>/delete/', views.inspection_type_delete, name='inspection_type_delete'),
]
