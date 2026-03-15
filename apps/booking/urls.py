from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_trips, name='search_trips'),
    path('booking/seats/<int:trip_id>/', views.select_seats, name='select_seats'),
    path('booking/confirm/<int:trip_id>/', views.confirm_booking, name='confirm_booking'),
    path('booking/payment/<str:booking_ref>/', views.booking_payment, name='booking_payment'),
    path('booking/verify-payment/', views.verify_payment, name='verify_payment'),
    path('booking/ticket/<str:booking_ref>/', views.booking_ticket, name='booking_ticket'),
    path('booking/detail/<str:booking_ref>/', views.booking_detail, name='booking_detail'),
    path('booking/my-bookings/', views.my_bookings, name='my_bookings'),
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/create/', views.trip_create, name='trip_create'),
    path('trips/<int:pk>/edit/', views.trip_edit, name='trip_edit'),
    path('api/seats/<int:trip_id>/', views.get_seat_availability, name='seat_availability'),
]
