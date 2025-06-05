from django.urls import path
from . import views

app_name = 'petpaths'

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/route/', views.route_api, name='route_api'),
]