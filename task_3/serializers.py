from rest_framework import serializers
from .models import *



class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"

class InventoryItemNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'quantity']

class ServiceBookingSerializer(serializers.ModelSerializer):
    # service_items = InventoryItemNestedSerializer(many=True)
    class Meta:
        model = ServiceBooking
        exclude = ['service_items']

class ServiceBookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBookingItem
        fields = "__all__"












