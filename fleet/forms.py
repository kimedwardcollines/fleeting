from django import forms
from .models import Vehicle, Driver, Trip, Maintenance, FuelRecord
from datetime import date


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_id', 'registration_number', 'vehicle_type', 'make', 'model', 
                  'year', 'capacity', 'status', 'assigned_driver', 'fuel_type', 'mileage', 'last_service_date']
        widgets = {
            'last_service_date': forms.DateInput(attrs={'type': 'date'}),
            'year': forms.NumberInput(attrs={'min': 1990, 'max': 2030}),
        }


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['employee_id', 'full_name', 'license_number', 'license_expiry', 
                  'phone_number', 'email', 'address', 'status', 'assigned_vehicle']
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
        }


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['driver', 'vehicle', 'origin', 'destination', 'distance', 
                  'departure_date', 'arrival_date', 'status', 'cargo_type', 'cargo_weight', 'fuel_consumed', 'notes']
        widgets = {
            'departure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['vehicle', 'service_type', 'description', 'service_date', 
                  'completion_date', 'cost', 'mileage_at_service', 'mechanic_name', 'status', 'notes']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }


class FuelRecordForm(forms.ModelForm):
    class Meta:
        model = FuelRecord
        fields = ['vehicle', 'driver', 'trip', 'liters', 'price_per_liter', 
                  'odometer_reading', 'fuel_type', 'station', 'date', 'receipt_number', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        liters = cleaned_data.get('liters')
        price = cleaned_data.get('price_per_liter')
        if liters and price:
            cleaned_data['total_cost'] = liters * price
        return cleaned_data