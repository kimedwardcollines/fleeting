from django.urls import path
from . import views

app_name = 'fleet'

urlpatterns = [
    # Dashboard
    path('', views.fleet_dashboard, name='dashboard'),
    
    # Vehicle URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicles/<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # Driver URLs
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_add, name='driver_add'),
    path('drivers/<int:pk>/edit/', views.driver_edit, name='driver_edit'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    
    # Trip URLs
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.trip_add, name='trip_add'),
    path('trips/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trips/<int:pk>/edit/', views.trip_edit, name='trip_edit'),
    
    # Maintenance URLs
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/add/', views.maintenance_add, name='maintenance_add'),
    
    # Fuel URLs
    path('fuel/', views.fuel_list, name='fuel_list'),
    path('fuel/add/', views.fuel_add, name='fuel_add'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
]