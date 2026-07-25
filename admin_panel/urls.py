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
    path('api/students/',                         views.admin_students_api,          name='admin_students'),
    
    # Auth APIs
    path('api/auth/status/',                      views.auth_status_api,             name='auth_status'),
    path('api/auth/student_login/',               views.student_login_api,           name='student_login_api'),

    # ClickUp Integration API
    path('api/clickup/sync/',                     views.clickup_sync_api,            name='clickup_sync'),
    path('api/clickup/config/',                   views.clickup_config_api,          name='clickup_config'),
    path('api/clickup/status/',                   views.clickup_status_api,          name='clickup_status'),
]
