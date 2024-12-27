from django.contrib import admin
from .models import Dealer, Customer, Vehicle, ServiceBooking

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('id', 'dealer_name', 'contact_number', 'email', 'address')
    search_fields = ('dealer_name', 'contact_number', 'email')
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'contact_number', 'email', 'address')
    search_fields = ('customer_name', 'contact_number', 'email')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_registration_number', 'brand', 'model', 'year_of_manufacture', 'customer')
    search_fields = ('vehicle_registration_number', 'brand', 'model')
    list_filter = ('year_of_manufacture',)

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking_date', 'service_date', 'service_type', 'vehicle', 'dealer')
    search_fields = ('service_type',)
    list_filter = ('service_date',)
