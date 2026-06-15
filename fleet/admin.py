from django.contrib import admin
from .models import Vehicle, Driver, Trip, Maintenance, FuelRecord


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_id', 'registration_number', 'vehicle_type', 'make', 'status', 'assigned_driver']
    list_filter = ['status', 'vehicle_type', 'fuel_type']
    search_fields = ['vehicle_id', 'registration_number', 'make', 'model']


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'license_number', 'status', 'assigned_vehicle']
    list_filter = ['status']
    search_fields = ['employee_id', 'full_name', 'license_number']


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ['trip_id', 'driver', 'vehicle', 'origin', 'destination', 'status', 'departure_date']
    list_filter = ['status']
    search_fields = ['trip_id', 'origin', 'destination']


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'service_type', 'service_date', 'cost', 'status']
    list_filter = ['status', 'service_type']
    search_fields = ['vehicle__registration_number']


@admin.register(FuelRecord)
class FuelRecordAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'driver', 'liters', 'total_cost', 'date']
    list_filter = ['fuel_type']
    search_fields = ['vehicle__registration_number', 'driver__full_name']