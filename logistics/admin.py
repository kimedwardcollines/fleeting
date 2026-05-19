from django.contrib import admin
from .models import Booking
import secrets


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Display columns
    list_display = ('tracking_number', 'name', 'service_type', 'status', 
                   'pickup_location', 'destination', 'estimated_price', 'booked_time')
    
    # Add custom method to display time clearly
    @admin.display(description='Booked At', ordering='created_at')
    def booked_time(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S') if obj.created_at else '-'
    
    # Filters
    list_filter = ('status', 'service_type', 'currency', 'created_at')
    
    # Search
    search_fields = ('name', 'phone', 'tracking_number', 'delivery_code', 'email',
                   'pickup_location', 'destination')
    
    # Order by newest first
    ordering = ('-created_at',)
    
    # Read-only fields (auto-generated)
    readonly_fields = ('tracking_number', 'delivery_code', 'created_at', 
                      'calculated_distance')
    
    # Date hierarchy
    date_hierarchy = 'created_at'
    
    # List per page
    list_per_page = 25
    
    # Fields to show in detail view - organized in sections
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'phone', 'email')
        }),
        ('Service Details', {
            'fields': ('service_type', 'pickup_location', 'destination', 
                      'calculated_distance', 'estimated_price', 'currency')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_number', 'delivery_code', 
                       'delivery_verified', 'date', 'message', 'created_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Generate delivery code when status changes to in_transit via admin"""
        if change and obj.status == 'in_transit' and not obj.delivery_code:
            if not obj._state.adding:  # This is an existing object being edited
                obj.delivery_code = secrets.token_hex(3).upper()
        super().save_model(request, obj, form, change)
