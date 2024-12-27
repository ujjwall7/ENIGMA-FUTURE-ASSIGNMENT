from django.urls import path
from . import views

urlpatterns = [
    path('inventory_item/', views.InventoryItemAPI.as_view()),
    path('service_booking/', views.ServiceBookingAPI.as_view()),
    path('service_booking_item/', views.ServiceBookingItemAPI.as_view()),
]


