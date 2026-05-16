from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'phone', 'email', 'pickup_location', 'destination', 'date', 'created_at')
    list_filter = ('service_type', 'created_at')
    search_fields = ('name', 'phone', 'email')
