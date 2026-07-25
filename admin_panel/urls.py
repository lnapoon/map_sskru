from django.urls import path
from . import views

urlpatterns = [
    path('',           views.admin_login_page,          name='admin_login'),
    path('login/',     views.admin_login_page,          name='admin_login_slash'),
    path('logout/',    views.admin_logout,              name='admin_logout'),
    path('dashboard/', views.admin_dashboard,           name='admin_dashboard'),

    # Admin Building CRUD API
    path('api/buildings/',                        views.admin_buildings_api,         name='admin_buildings'),
    path('api/buildings/<int:building_id>/',      views.admin_building_detail_api,   name='admin_building_detail'),
    path('api/analytics/',                        views.admin_analytics_api,         name='admin_analytics'),
]
