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
    path('api/auth/student_request_reset/',       views.student_request_reset_api,   name='student_request_reset_api'),
    path('api/auth/student_verify_reset_token/',  views.student_verify_reset_token_api, name='student_verify_reset_token_api'),
    path('api/auth/student_confirm_new_password/', views.student_confirm_new_password_api, name='student_confirm_new_password_api'),

    # Dedicated Register & Password Reset Pages
    path('register/student/',                     views.student_register_page,       name='student_register_page'),
    path('register/staff/',                       views.staff_register_page,         name='staff_register_page'),
    path('reset_password/student/',               views.student_reset_password_page, name='student_reset_password_page'),
    path('reset_password/student/verify/',        views.student_reset_password_verify_page, name='student_reset_password_verify_page'),
]
