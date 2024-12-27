from django.db import models

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.dealer_name

class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.customer_name

class Vehicle(models.Model):
    vehicle_registration_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year_of_manufacture = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vehicles')

    def __str__(self):
        return self.vehicle_registration_number

class ServiceBooking(models.Model):
    booking_date = models.DateField()
    service_date = models.DateField()
    service_type = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle')
    dealer = models.ForeignKey(Dealer, on_delete=models.SET_NULL, null=True, related_name='dealer')

    def __str__(self):
        return f"Booking {self.id} for {self.vehicle}"
