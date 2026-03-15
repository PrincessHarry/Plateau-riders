from django.contrib import admin
from .models import Bus, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = ['seat_number']

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'bus_type', 'capacity', 'is_active']
    list_filter = ['bus_type', 'is_active']
    inlines = [SeatInline]

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['bus', 'seat_number']
    list_filter = ['bus']
