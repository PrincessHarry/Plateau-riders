from django.urls import path
from . import views

urlpatterns = [
    path('', views.route_list, name='route_list'),
    path('create/', views.route_create, name='route_create'),
    path('<int:pk>/stops/', views.route_stops, name='route_stops'),
]
