from django.urls import path
from . import views

urlpatterns = [
    path('', views.bus_list, name='bus_list'),
    path('create/', views.bus_create, name='bus_create'),
]
