from django.db import models

class ServiceRecord(models.Model):
    owner_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    service_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.owner_name} - {self.vehicle_model}"
