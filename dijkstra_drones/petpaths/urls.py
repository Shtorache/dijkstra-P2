from django.urls import path
from . import views

app_name = 'petpaths'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/route/', views.route_api, name='route_api'),
    path('map/', views.map_view, name='map'),
    ]