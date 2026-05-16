from django.db import models

# Create your models here.

class Booking(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('cargo', 'Cargo Logistics'),
        ('passenger', 'Passenger Transport'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    pickup_location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"
