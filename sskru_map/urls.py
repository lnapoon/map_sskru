from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from api.views import index_view
from api import views as api_views
from admin_panel import views as admin_views

from admin_panel.views import track_event, student_login_page

urlpatterns = [
    path('', index_view, name='index'),
    path('login/', admin_views.student_login_page, name='student_login'),
    path('register/student/', admin_views.student_register_page, name='student_register_page'),
    path('register/staff/', admin_views.staff_register_page, name='staff_register_page'),
    path('reset_password/student/', admin_views.student_reset_password_page, name='student_reset_password_page'),
    path('reset_password/student/verify/', admin_views.student_reset_password_verify_page, name='student_reset_password_verify_page'),
    path('reset_password/staff/', admin_views.staff_reset_password_page, name='staff_reset_password_page'),
    path('reset_password/staff/verify/', admin_views.staff_reset_password_verify_page, name='staff_reset_password_verify_page'),
    path('logout/', api_views.logout_view, name='logout'),
    path('admin/', include('admin_panel.urls')),
    path('api/track', track_event, name='track_event'),
    path('api/', include('api.urls')),
    re_path(r'^(?P<path>(assets/.*|images/.*|manifest\.json|favicon\.ico|app\.js|styles\.css|sw\.js))$', serve, {'document_root': settings.BASE_DIR}),
]
