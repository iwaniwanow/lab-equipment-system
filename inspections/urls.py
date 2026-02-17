from django.urls import path
from . import views

urlpatterns = [
    path('inspections/', views.inspection_list, name='inspection_list'),
    path('inspections/<int:pk>/', views.inspection_detail, name='inspection_detail'),
    path('inspections/create/', views.inspection_create, name='inspection_create'),
    path('inspections/<int:pk>/update/', views.inspection_update, name='inspection_update'),
    path('inspections/<int:pk>/delete/', views.inspection_delete, name='inspection_delete'),
]
