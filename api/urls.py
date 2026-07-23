from django.urls import path
from . import views

urlpatterns = [
    path('health', views.health_check),
    path('health/', views.health_check),
    path('admin/login', views.admin_login),
    path('admin/login/', views.admin_login),
    path('buildings', views.buildings_list),
    path('buildings/', views.buildings_list),
    path('buildings/<int:building_id>', views.building_detail),
    path('buildings/<int:building_id>/', views.building_detail),
]
