"""
Analytics App Models
Analytics and reporting for shipments and business metrics
"""

import uuid
from django.db import models
from apps.users.models import CustomUser
from apps.shipments.models import Shipment


class ShipmentAnalytics(models.Model):
    """
    Daily analytics for shipments
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    date = models.DateField(db_index=True)
    
    # Shipment Counts
    total_shipments = models.PositiveIntegerField(default=0)
    delivered_shipments = models.PositiveIntegerField(default=0)
    failed_shipments = models.PositiveIntegerField(default=0)
    cancelled_shipments = models.PositiveIntegerField(default=0)
    in_transit_shipments = models.PositiveIntegerField(default=0)
    
    # Revenue
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Performance
    on_time_delivery_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    average_delivery_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # hours
    successful_first_attempt = models.PositiveIntegerField(default=0)
    
    # Volume
    total_weight_shipped = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # kg
    avg_shipment_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'shipment_analytics'
        ordering = ['-date']
        unique_together = ['date']
    
    def __str__(self):
        return f"Analytics - {self.date}"


class UserAnalytics(models.Model):
    """
    User-level analytics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='analytics')
    
    # Activity
    total_shipments_sent = models.PositiveIntegerField(default=0)
    total_shipments_received = models.PositiveIntegerField(default=0)
    
    # Financial
    total_amount_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_amount_saved = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # discounts
    
    # Performance
    avg_delivery_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # hours
    on_time_delivery_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    
    # Engagement
    last_shipment_date = models.DateField(blank=True, null=True)
    total_logins = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_analytics'
    
    def __str__(self):
        return f"Analytics - {self.user.email}"


class RegionAnalytics(models.Model):
    """
    Analytics by delivery region/area
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    region = models.CharField(max_length=100, unique=True, db_index=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    # Shipment Metrics
    total_shipments = models.PositiveIntegerField(default=0)
    successful_deliveries = models.PositiveIntegerField(default=0)
    failed_deliveries = models.PositiveIntegerField(default=0)
    avg_delivery_time = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Network Metrics
    active_couriers = models.PositiveIntegerField(default=0)
    distribution_hubs = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'region_analytics'
    
    def __str__(self):
        return self.region


class RevenueReport(models.Model):
    """
    Monthly/Yearly revenue reports
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    report_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ]
    )
    
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Revenue
    shipping_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    service_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Costs
    operational_costs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    personnel_costs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_costs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Profit
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Transactions
    transaction_count = models.PositiveIntegerField(default=0)
    avg_transaction_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'revenue_reports'
        ordering = ['-period_end']
    
    def __str__(self):
        return f"{self.report_type.title()} Report - {self.period_start} to {self.period_end}"
