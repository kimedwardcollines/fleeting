from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Display columns
    list_display = ('name', 'phone', 'service_type', 'pickup_location', 'destination', 'calculated_distance', 'estimated_price', 'currency', 'date', 'created_at')
    
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
    
    # Fields to show in detail view
    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Trip Details', {
            'fields': ('service_type', 'pickup_location', 'destination', 'calculated_distance', 'estimated_price', 'date')
        }),
        ('Additional', {
            'fields': ('message', 'created_at')
        }),
    )
