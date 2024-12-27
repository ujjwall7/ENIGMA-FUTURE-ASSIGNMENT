from django.contrib import admin
from . models import *

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('owner_name', 'vehicle_model', 'service_date', 'description', )
    list_display_links = ('owner_name', 'vehicle_model', 'service_date', 'description', )



