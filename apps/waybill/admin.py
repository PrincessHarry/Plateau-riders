from django.contrib import admin
from .models import Waybill, WaybillStatusHistory

class WaybillStatusHistoryInline(admin.TabularInline):
    model = WaybillStatusHistory
    extra = 0
    readonly_fields = ['updated_at']

@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'sender_name', 'receiver_name', 'origin', 'destination', 'status', 'weight', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_code', 'sender_name', 'receiver_name', 'sender_phone', 'receiver_phone']
    readonly_fields = ['tracking_code', 'created_at', 'updated_at']
    inlines = [WaybillStatusHistoryInline]

@admin.register(WaybillStatusHistory)
class WaybillStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['waybill', 'status', 'updated_by', 'updated_at']
    list_filter = ['status', 'updated_at']
