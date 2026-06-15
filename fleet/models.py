from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date, timedelta


class Vehicle(models.Model):
    """Vehicle model for fleet management"""
    
    VEHICLE_TYPE_CHOICES = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('pickup', 'Pickup'),
        ('bus', 'Bus'),
        ('sedan', 'Sedan'),
    ]
    
    MAKE_CHOICES = [
        ('Toyota', 'Toyota'),
        ('Isuzu', 'Isuzu'),
        ('Ford', 'Ford'),
        ('Nissan', 'Nissan'),
        ('Mitsubishi', 'Mitsubishi'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Hyundai', 'Hyundai'),
        ('Kia', 'Kia'),
        ('Yutong', 'Yutong'),
        ('King Long', 'King Long'),
        ('Hino', 'Hino'),
        ('DAF', 'DAF'),
        ('Volvo', 'Volvo'),
        ('Scania', 'Scania'),
        ('MAN', 'MAN'),
    ]
    
    YEAR_CHOICES = [(year, str(year)) for year in range(2015, 2027)]
    
    CAPACITY_TONNES_CHOICES = [
        ('1', '1 Ton'),
        ('2', '2 Tons'),
        ('3', '3 Tons'),
        ('5', '5 Tons'),
        ('7', '7 Tons'),
        ('10', '10 Tons'),
        ('15', '15 Tons'),
        ('20', '20 Tons'),
        ('25', '25 Tons'),
        ('30', '30 Tons'),
    ]
    
    CAPACITY_PASSENGERS_CHOICES = [
        ('5', '5 Passengers'),
        ('7', '7 Passengers'),
        ('12', '12 Passengers'),
        ('14', '14 Passengers'),
        ('18', '18 Passengers'),
        ('25', '25 Passengers'),
        ('30', '30 Passengers'),
        ('35', '35 Passengers'),
        ('40', '40 Passengers'),
        ('50', '50 Passengers'),
        ('60', '60 Passengers'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('out_of_service', 'Out of Service'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('diesel', 'Diesel'),
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    vehicle_id = models.CharField(max_length=20, unique=True, help_text="Unique vehicle identifier")
    registration_number = models.CharField(max_length=20, unique=True, help_text="License plate number")
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    make = models.CharField(max_length=50, choices=MAKE_CHOICES, help_text="Vehicle make/manufacturer")
    model = models.CharField(max_length=50, help_text="Vehicle model")
    year = models.IntegerField(choices=YEAR_CHOICES, help_text="Manufacturing year")
    capacity_tonnes = models.CharField(max_length=10, choices=CAPACITY_TONNES_CHOICES, blank=True, null=True, help_text="Cargo capacity in tonnes")
    capacity_passengers = models.CharField(max_length=10, choices=CAPACITY_PASSENGERS_CHOICES, blank=True, null=True, help_text="Passenger capacity")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    assigned_driver = models.ForeignKey(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_vehicles'
    )
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='diesel')
    mileage = models.IntegerField(default=0, help_text="Current mileage in km")
    last_service_date = models.DateField(null=True, blank=True)
    next_service_due = models.DateField(null=True, blank=True, help_text="Next scheduled service date")
    service_interval_days = models.IntegerField(default=90, help_text="Service interval in days")
    mileage_interval = models.IntegerField(default=5000, help_text="Service interval in km")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Vehicles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.vehicle_id} - {self.registration_number}"
    
    def get_days_since_last_service(self):
        """Returns days since last service"""
        if not self.last_service_date:
            return None
        return (date.today() - self.last_service_date).days
    
    def get_kms_since_last_service(self):
        """Returns km since last service (approximate based on mileage)"""
        if not self.last_service_date:
            return self.mileage
        # Estimate average 200km per day
        days = self.get_days_since_last_service()
        if days:
            estimated_mileage_at_service = self.mileage - (days * 200)
            return max(0, self.mileage - max(0, estimated_mileage_at_service))
        return 0
    
    def is_maintenance_due(self):
        """Check if maintenance is due based on time or mileage"""
        if not self.last_service_date:
            return True
        
        days_since_service = self.get_days_since_last_service()
        kms_since_service = self.get_kms_since_last_service()
        
        # Check if either time interval OR mileage interval exceeded
        if days_since_service and days_since_service >= self.service_interval_days:
            return True
        if kms_since_service and kms_since_service >= self.mileage_interval:
            return True
        return False
    
    def get_recommended_service(self):
        """Returns the recommended service type based on usage"""
        if not self.last_service_date:
            return 'inspection'
        
        days_since_service = self.get_days_since_last_service() or 0
        kms_since_service = self.get_kms_since_last_service() or 0
        
        # Heavy usage (>10000km or >60 days): Full service
        if kms_since_service > 10000 or days_since_service > 60:
            return 'engine_repair'
        
        # Medium usage (>5000km or >45 days): Intermediate service
        if kms_since_service > 5000 or days_since_service > 45:
            return 'oil_change'
        
        # Light overdue: Basic check
        if self.is_maintenance_due():
            return 'inspection'
        
        # Regular maintenance
        return 'oil_change'
    
    def get_service_description(self):
        """Returns a description of what service is needed"""
        service_type = self.get_recommended_service()
        descriptions = {
            'oil_change': f'Oil change and filter replacement. Vehicle {self.registration_number} has traveled approximately {self.get_kms_since_last_service():,} km since last service.',
            'tire_rotation': f'Tire rotation and pressure check for {self.registration_number}.',
            'brake_service': f'Brake inspection and service for {self.registration_number}.',
            'engine_repair': f'Comprehensive engine service for {self.registration_number}. Heavy usage detected.',
            'transmission': f'Transmission check for {self.registration_number}.',
            'electrical': f'Electrical system inspection for {self.registration_number}.',
            'body_work': f'Body work assessment for {self.registration_number}.',
            'inspection': f'General inspection for {self.registration_number}. Service is overdue.',
            'other': f'Service maintenance for {self.registration_number}.',
        }
        return descriptions.get(service_type, f'Service for {self.registration_number}.')
    
    def get_next_service_date(self):
        """Calculate the next service date based on last service"""
        if self.last_service_date:
            return self.last_service_date + timedelta(days=self.service_interval_days)
        return date.today()
    
    def save(self, *args, **kwargs):
        # Auto-calculate next service due date
        if self.last_service_date:
            self.next_service_due = self.last_service_date + timedelta(days=self.service_interval_days)
        super().save(*args, **kwargs)


class Driver(models.Model):
    """Driver model for fleet management"""
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
    ]
    
    employee_id = models.CharField(max_length=20, unique=True, help_text="Employee ID")
    full_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=30, unique=True)
    license_expiry = models.DateField(help_text="License expiry date")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    assigned_vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_driver'
    )
    date_joined = models.DateField(auto_now_add=True)
    total_trips = models.IntegerField(default=0)
    total_distance = models.IntegerField(default=0, help_text="Total distance driven in km")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"


class Trip(models.Model):
    """Trip model for fleet management"""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    trip_id = models.CharField(max_length=20, unique=True, help_text="Unique trip identifier")
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='trips'
    )
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.IntegerField(help_text="Distance in km")
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    cargo_type = models.CharField(max_length=100, blank=True)
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    fuel_consumed = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text="Fuel consumed in liters")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Trips"
        ordering = ['-departure_date']
    
    def save(self, *args, **kwargs):
        if not self.trip_id:
            import uuid
            year = 2026
            unique_id = uuid.uuid4().hex[:6].upper()
            self.trip_id = f'TR-{year}-{unique_id}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.trip_id}: {self.origin} to {self.destination}"


class Maintenance(models.Model):
    """Maintenance model for fleet management"""
    
    SERVICE_TYPE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('tire_rotation', 'Tire Rotation'),
        ('brake_service', 'Brake Service'),
        ('engine_repair', 'Engine Repair'),
        ('transmission', 'Transmission'),
        ('electrical', 'Electrical'),
        ('body_work', 'Body Work'),
        ('inspection', 'Inspection'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )
    service_type = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    description = models.TextField()
    service_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    mileage_at_service = models.IntegerField(null=True, blank=True)
    mechanic_name = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Maintenance Records"
        ordering = ['-service_date']
    
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.get_service_type_display()} on {self.service_date}"


class FuelRecord(models.Model):
    """Fuel record model for fleet management"""
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='fuel_records'
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='fuel_records'
    )
    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fuel_records'
    )
    liters = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    price_per_liter = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    odometer_reading = models.IntegerField(help_text="Odometer reading in km")
    fuel_type = models.CharField(max_length=20, choices=[('diesel', 'Diesel'), ('petrol', 'Petrol')], default='diesel')
    station = models.CharField(max_length=100, blank=True, help_text="Gas station name")
    date = models.DateField()
    receipt_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Fuel Records"
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        self.total_cost = self.liters * self.price_per_liter
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.liters}L on {self.date}"