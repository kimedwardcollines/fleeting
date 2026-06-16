from django.db import models
from datetime import datetime


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
    delivery_code = models.CharField(max_length=10, blank=True, help_text="Code for customer to verify delivery")
    delivery_verified = models.BooleanField(default=False)
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
        is_new = not self.pk  # Check if this is a new booking
        
        if not self.tracking_number:
            import uuid
            year = datetime.now().year
            unique_id = uuid.uuid4().hex[:8].upper()
            self.tracking_number = f'FL-{year}-{unique_id}'
        
        # Generate delivery code when status changes to in_transit
        if self.status == 'in_transit' and not self.delivery_code:
            import secrets
            self.delivery_code = secrets.token_hex(3).upper()
        
        super().save(*args, **kwargs)
        
        # Create fleet trip when booking is created
        if is_new and self.tracking_number:
            self._create_fleet_trip()
    
    def _create_fleet_trip(self):
        """Create a corresponding trip in fleet management"""
        try:
            from fleet.models import Trip
            # Check if trip already exists
            if not Trip.objects.filter(trip_id=self.tracking_number).exists():
                Trip.objects.create(
                    trip_id=self.tracking_number,
                    origin=self.pickup_location,
                    destination=self.destination,
                    distance=self.calculated_distance or 0,
                    status='scheduled',
                    cargo_type=self.get_service_type_display(),
                    notes=f"Customer: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nBooking Price: {self.currency} {self.estimated_price}"
                )
        except Exception as e:
            # Log error but don't fail booking creation
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create fleet trip for booking {self.tracking_number}: {e}")
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} - ${self.estimated_price}"
