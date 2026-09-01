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
    path('api/auth/student_verify/',              views.student_verify_api,          name='student_verify_api'),
    path('api/auth/student_register/',            views.student_register_api,        name='student_register_api'),
    path('api/auth/staff_register/',              views.staff_register_api,          name='staff_register_api'),
    path('api/auth/staff_login/',                 views.staff_login_api,             name='staff_login_api'),

    # Dedicated Register Pages
    path('register/student/',                     views.student_register_page,       name='student_register_page'),
    path('register/staff/',                       views.staff_register_page,         name='staff_register_page'),
]
