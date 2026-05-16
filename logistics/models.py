from django.db import models
from datetime import datetime

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
    tracking_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
    ], default='pending')
    date = models.DateField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            import random
            import string
            year = datetime.now().year
            random_id = ''.join(random.choices(string.digits, k=3))
            self.tracking_number = f'FL-{year}-{random_id}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} - ${self.estimated_price}"
