from django.contrib import admin
from .models import Route, RouteStop

class RouteStopInline(admin.TabularInline):
    model = RouteStop
    extra = 3
    ordering = ['order']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['origin', 'destination', 'base_price', 'is_active']
    list_filter = ['is_active']
    inlines = [RouteStopInline]

@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    list_display = ['route', 'location', 'order', 'price_from_origin']
    list_filter = ['route']
    ordering = ['route', 'order']
