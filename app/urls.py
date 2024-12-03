# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import product_detail_view


urlpatterns = [
    path('', views.index, name='index'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)