from django.contrib import admin
from .models import Trip, Booking

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['route', 'bus', 'departure_time', 'price', 'status', 'available_seat_count']
    list_filter = ['status', 'departure_time']
    search_fields = ['route__origin', 'route__destination', 'bus__plate_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'passenger_name', 'trip', 'seat', 'start_stop', 'end_stop', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['booking_reference', 'passenger_name', 'phone']
    readonly_fields = ['booking_reference', 'created_at']
