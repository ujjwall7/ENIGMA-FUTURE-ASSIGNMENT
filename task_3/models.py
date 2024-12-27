from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ServiceBooking(models.Model):
    customer_name = models.CharField(max_length=255)
    vehicle_details = models.CharField(max_length=255)
    service_date = models.DateTimeField()
    service_items = models.ManyToManyField(
        InventoryItem, related_name='service_items'
        )
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.customer_name} on {self.service_date}"

class ServiceBookingItem(models.Model):
    booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} for Booking ID {self.booking.id}"
