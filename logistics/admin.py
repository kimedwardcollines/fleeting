from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Display columns
    list_display = ('name', 'phone', 'service_type', 'pickup_location', 'destination', 'date', 'created_at')
    
    # Filters
    list_filter = ('service_type', 'date')
    
    # Search
    search_fields = ('name', 'phone')
    
    # Order by newest first
    ordering = ('-created_at',)
    
    # Read-only fields
    readonly_fields = ('created_at',)
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # List per page
    list_per_page = 20
