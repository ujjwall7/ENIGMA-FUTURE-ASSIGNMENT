from django.contrib import admin
from .models import InventoryItem, ServiceBooking, ServiceBookingItem

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'vehicle_details', 'service_date', 'total_cost', 'created_at', 'updated_at')
    search_fields = ('customer_name', 'vehicle_details')
    list_filter = ('service_date', 'created_at')

@admin.register(ServiceBookingItem)
class ServiceBookingItemAdmin(admin.ModelAdmin):
    list_display = ('booking', 'item', 'quantity', 'cost')
    search_fields = ('booking__customer_name', 'item__name')
    list_filter = ('booking__service_date',)
