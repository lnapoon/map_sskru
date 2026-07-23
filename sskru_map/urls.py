from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from api.views import index_view

urlpatterns = [
    path('', index_view, name='index'),
    path('api/', include('api.urls')),
    re_path(r'^(?P<path>(app\.js|styles\.css|Map\.png|images/.*))$', serve, {'document_root': settings.BASE_DIR}),
]
