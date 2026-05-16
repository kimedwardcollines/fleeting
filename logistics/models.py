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
    calculated_distance = models.IntegerField(default=0, help_text="Distance in kilometers")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Estimated price in USD")
    currency = models.CharField(max_length=3, choices=[('USD', 'USD'), ('UGX', 'UGX')], default='USD')
    date = models.DateField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} - ${self.estimated_price}"
