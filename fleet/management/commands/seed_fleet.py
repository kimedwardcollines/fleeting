from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from decimal import Decimal
import random
from fleet.models import Vehicle, Driver, Trip, Maintenance, FuelRecord


# ============================================================
# SEED DATA - UPDATE THESE DETAILS FOR YOUR LOCAL DEVELOPMENT
# ============================================================

# Vehicle Types: truck, van, pickup, bus, sedan
# Makes: Toyota, Isuzu, Ford, Nissan, Mitsubishi, Mercedes-Benz, Hyundai, Kia, 
#        Yutong, King Long, Hino, DAF, Volvo, Scania, MAN
# Status: active, maintenance, out_of_service
# Fuel Type: diesel, petrol, electric, hybrid

VEHICLES = [
    # V1 - V10: Trucks
    {'vehicle_id': 'V1', 'registration_number': 'XXX 001A', 'vehicle_type': 'truck', 'make': 'Isuzu', 'model': 'NPR', 'year': 2022, 'capacity_tonnes': '5', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 45000},
    {'vehicle_id': 'V2', 'registration_number': 'XXX 002A', 'vehicle_type': 'truck', 'make': 'Hino', 'model': '300', 'year': 2021, 'capacity_tonnes': '10', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 62000},
    {'vehicle_id': 'V3', 'registration_number': 'XXX 003A', 'vehicle_type': 'truck', 'make': 'Mitsubishi', 'model': 'Fuso', 'year': 2020, 'capacity_tonnes': '10', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 85000},
    {'vehicle_id': 'V4', 'registration_number': 'XXX 004A', 'vehicle_type': 'truck', 'make': 'DAF', 'model': 'LF', 'year': 2022, 'capacity_tonnes': '15', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 38000},
    {'vehicle_id': 'V5', 'registration_number': 'XXX 005A', 'vehicle_type': 'truck', 'make': 'Volvo', 'model': 'FH', 'year': 2021, 'capacity_tonnes': '20', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 72000},
    {'vehicle_id': 'V6', 'registration_number': 'XXX 006A', 'vehicle_type': 'truck', 'make': 'Scania', 'model': 'G-series', 'year': 2020, 'capacity_tonnes': '25', 'status': 'maintenance', 'fuel_type': 'diesel', 'mileage': 95000},
    {'vehicle_id': 'V7', 'registration_number': 'XXX 007A', 'vehicle_type': 'truck', 'make': 'MAN', 'model': 'TGM', 'year': 2023, 'capacity_tonnes': '7', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 25000},
    {'vehicle_id': 'V8', 'registration_number': 'XXX 008A', 'vehicle_type': 'truck', 'make': 'Isuzu', 'model': 'NQR', 'year': 2022, 'capacity_tonnes': '3', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 52000},
    {'vehicle_id': 'V9', 'registration_number': 'XXX 009A', 'vehicle_type': 'truck', 'make': 'Hino', 'model': '500', 'year': 2021, 'capacity_tonnes': '15', 'status': 'out_of_service', 'fuel_type': 'diesel', 'mileage': 110000},
    {'vehicle_id': 'V10', 'registration_number': 'XXX 010A', 'vehicle_type': 'truck', 'make': 'Mercedes-Benz', 'model': 'Actros', 'year': 2022, 'capacity_tonnes': '30', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 48000},
    
    # V11 - V15: Vans
    {'vehicle_id': 'V11', 'registration_number': 'XXX 011A', 'vehicle_type': 'van', 'make': 'Toyota', 'model': 'Hiace', 'year': 2023, 'capacity_passengers': '12', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 28000},
    {'vehicle_id': 'V12', 'registration_number': 'XXX 012A', 'vehicle_type': 'van', 'make': 'Mercedes-Benz', 'model': 'Sprinter', 'year': 2023, 'capacity_passengers': '12', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 15000},
    {'vehicle_id': 'V13', 'registration_number': 'XXX 013A', 'vehicle_type': 'van', 'make': 'Ford', 'model': 'Transit', 'year': 2022, 'capacity_passengers': '14', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 42000},
    {'vehicle_id': 'V14', 'registration_number': 'XXX 014A', 'vehicle_type': 'van', 'make': 'Nissan', 'model': 'NV350', 'year': 2021, 'capacity_passengers': '12', 'status': 'maintenance', 'fuel_type': 'petrol', 'mileage': 65000},
    {'vehicle_id': 'V15', 'registration_number': 'XXX 015A', 'vehicle_type': 'van', 'make': 'Hyundai', 'model': 'Starex', 'year': 2022, 'capacity_passengers': '7', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 35000},
    
    # V16 - V20: Pickups
    {'vehicle_id': 'V16', 'registration_number': 'XXX 016A', 'vehicle_type': 'pickup', 'make': 'Ford', 'model': 'Ranger', 'year': 2022, 'capacity_tonnes': '1', 'status': 'maintenance', 'fuel_type': 'diesel', 'mileage': 38000},
    {'vehicle_id': 'V17', 'registration_number': 'XXX 017A', 'vehicle_type': 'pickup', 'make': 'Nissan', 'model': 'Navara', 'year': 2022, 'capacity_tonnes': '1', 'status': 'out_of_service', 'fuel_type': 'diesel', 'mileage': 72000},
    {'vehicle_id': 'V18', 'registration_number': 'XXX 018A', 'vehicle_type': 'pickup', 'make': 'Toyota', 'model': 'Hilux', 'year': 2023, 'capacity_tonnes': '1', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 22000},
    {'vehicle_id': 'V19', 'registration_number': 'XXX 019A', 'vehicle_type': 'pickup', 'make': 'Isuzu', 'model': 'D-Max', 'year': 2021, 'capacity_tonnes': '1', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 55000},
    {'vehicle_id': 'V20', 'registration_number': 'XXX 020A', 'vehicle_type': 'pickup', 'make': 'Mitsubishi', 'model': 'L200', 'year': 2022, 'capacity_tonnes': '1', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 41000},
    
    # V21 - V25: Buses
    {'vehicle_id': 'V21', 'registration_number': 'XXX 021A', 'vehicle_type': 'bus', 'make': 'Yutong', 'model': 'ZK6105', 'year': 2021, 'capacity_passengers': '40', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 52000},
    {'vehicle_id': 'V22', 'registration_number': 'XXX 022A', 'vehicle_type': 'bus', 'make': 'King Long', 'model': 'XMQ6127', 'year': 2022, 'capacity_passengers': '50', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 38000},
    {'vehicle_id': 'V23', 'registration_number': 'XXX 023A', 'vehicle_type': 'bus', 'make': 'Toyota', 'model': 'Coaster', 'year': 2023, 'capacity_passengers': '25', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 18000},
    {'vehicle_id': 'V24', 'registration_number': 'XXX 024A', 'vehicle_type': 'bus', 'make': 'Yutong', 'model': 'ZK6858', 'year': 2020, 'capacity_passengers': '35', 'status': 'maintenance', 'fuel_type': 'diesel', 'mileage': 88000},
    {'vehicle_id': 'V25', 'registration_number': 'XXX 025A', 'vehicle_type': 'bus', 'make': 'Hino', 'model': 'RK8J', 'year': 2021, 'capacity_passengers': '60', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 62000},
    
    # V26 - V30: Sedans
    {'vehicle_id': 'V26', 'registration_number': 'XXX 026A', 'vehicle_type': 'sedan', 'make': 'Toyota', 'model': 'Camry', 'year': 2023, 'capacity_passengers': '5', 'status': 'active', 'fuel_type': 'hybrid', 'mileage': 12000},
    {'vehicle_id': 'V27', 'registration_number': 'XXX 027A', 'vehicle_type': 'sedan', 'make': 'Mercedes-Benz', 'model': 'E-Class', 'year': 2022, 'capacity_passengers': '5', 'status': 'active', 'fuel_type': 'petrol', 'mileage': 28000},
    {'vehicle_id': 'V28', 'registration_number': 'XXX 028A', 'vehicle_type': 'sedan', 'make': 'Hyundai', 'model': 'Sonata', 'year': 2023, 'capacity_passengers': '5', 'status': 'active', 'fuel_type': 'petrol', 'mileage': 15000},
    {'vehicle_id': 'V29', 'registration_number': 'XXX 029A', 'vehicle_type': 'sedan', 'make': 'Kia', 'model': 'K5', 'year': 2022, 'capacity_passengers': '5', 'status': 'active', 'fuel_type': 'petrol', 'mileage': 32000},
    {'vehicle_id': 'V30', 'registration_number': 'XXX 030A', 'vehicle_type': 'sedan', 'make': 'Toyota', 'model': 'Corolla', 'year': 2023, 'capacity_passengers': '5', 'status': 'active', 'fuel_type': 'hybrid', 'mileage': 8500},
]

# Driver Status: available, on_trip, on_leave, suspended
DRIVERS = [
    {'employee_id': 'D1', 'full_name': 'Driver Full Name 1', 'license_number': 'DL-001', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 001', 'email': 'driver1@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D2', 'full_name': 'Driver Full Name 2', 'license_number': 'DL-002', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 002', 'email': 'driver2@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D3', 'full_name': 'Driver Full Name 3', 'license_number': 'DL-003', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 003', 'email': 'driver3@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D4', 'full_name': 'Driver Full Name 4', 'license_number': 'DL-004', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 004', 'email': 'driver4@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D5', 'full_name': 'Driver Full Name 5', 'license_number': 'DL-005', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 005', 'email': 'driver5@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D6', 'full_name': 'Driver Full Name 6', 'license_number': 'DL-006', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 006', 'email': 'driver6@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D7', 'full_name': 'Driver Full Name 7', 'license_number': 'DL-007', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 007', 'email': 'driver7@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D8', 'full_name': 'Driver Full Name 8', 'license_number': 'DL-008', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 008', 'email': 'driver8@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D9', 'full_name': 'Driver Full Name 9', 'license_number': 'DL-009', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 009', 'email': 'driver9@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D10', 'full_name': 'Driver Full Name 10', 'license_number': 'DL-010', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 010', 'email': 'driver10@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D11', 'full_name': 'Driver Full Name 11', 'license_number': 'DL-011', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 011', 'email': 'driver11@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D12', 'full_name': 'Driver Full Name 12', 'license_number': 'DL-012', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 012', 'email': 'driver12@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D13', 'full_name': 'Driver Full Name 13', 'license_number': 'DL-013', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 013', 'email': 'driver13@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D14', 'full_name': 'Driver Full Name 14', 'license_number': 'DL-014', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 014', 'email': 'driver14@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D15', 'full_name': 'Driver Full Name 15', 'license_number': 'DL-015', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 015', 'email': 'driver15@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D16', 'full_name': 'Driver Full Name 16', 'license_number': 'DL-016', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 016', 'email': 'driver16@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D17', 'full_name': 'Driver Full Name 17', 'license_number': 'DL-017', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 017', 'email': 'driver17@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D18', 'full_name': 'Driver Full Name 18', 'license_number': 'DL-018', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 018', 'email': 'driver18@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D19', 'full_name': 'Driver Full Name 19', 'license_number': 'DL-019', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 019', 'email': 'driver19@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D20', 'full_name': 'Driver Full Name 20', 'license_number': 'DL-020', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 020', 'email': 'driver20@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D21', 'full_name': 'Driver Full Name 21', 'license_number': 'DL-021', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 021', 'email': 'driver21@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D22', 'full_name': 'Driver Full Name 22', 'license_number': 'DL-022', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 022', 'email': 'driver22@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D23', 'full_name': 'Driver Full Name 23', 'license_number': 'DL-023', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 023', 'email': 'driver23@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D24', 'full_name': 'Driver Full Name 24', 'license_number': 'DL-024', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 024', 'email': 'driver24@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D25', 'full_name': 'Driver Full Name 25', 'license_number': 'DL-025', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 025', 'email': 'driver25@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D26', 'full_name': 'Driver Full Name 26', 'license_number': 'DL-026', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 026', 'email': 'driver26@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D27', 'full_name': 'Driver Full Name 27', 'license_number': 'DL-027', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 027', 'email': 'driver27@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D28', 'full_name': 'Driver Full Name 28', 'license_number': 'DL-028', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 028', 'email': 'driver28@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D29', 'full_name': 'Driver Full Name 29', 'license_number': 'DL-029', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 029', 'email': 'driver29@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
    {'employee_id': 'D30', 'full_name': 'Driver Full Name 30', 'license_number': 'DL-030', 'license_expiry': date(2027, 6, 30), 'phone_number': '+256 700 000 030', 'email': 'driver30@company.com', 'status': 'available', 'total_trips': 0, 'total_distance': 0, 'rating': Decimal('5.00')},
]

# Trip Status: scheduled, in_progress, completed, cancelled
# Cargo Types: General Goods, Electronics, Food Items, Construction Materials, Textiles, Machinery, Chemicals
ROUTES = [
    ('City A', 'City B', 150),
    ('City A', 'City C', 220),
    ('City B', 'City A', 150),
    ('City B', 'City D', 180),
    ('City C', 'City A', 220),
    ('City C', 'City E', 300),
    ('City D', 'City B', 180),
    ('City D', 'City F', 250),
    ('City E', 'City C', 300),
    ('City E', 'City A', 350),
    ('Warehouse 1', 'Depot North', 80),
    ('Warehouse 1', 'Depot South', 120),
    ('Depot North', 'Warehouse 2', 90),
    ('Depot South', 'Warehouse 2', 100),
    ('City F', 'City D', 250),
]

TRIPS = [
    # T1 - T10: Completed trips
    {'trip_id': 'T1', 'driver_idx': 0, 'vehicle_idx': 0, 'route_idx': 0, 'status': 'completed', 'cargo_type': 'General Goods', 'cargo_weight': Decimal('2500'), 'departure_offset_days': -10, 'arrival_offset_hours': 3},
    {'trip_id': 'T2', 'driver_idx': 1, 'vehicle_idx': 1, 'route_idx': 1, 'status': 'completed', 'cargo_type': 'Electronics', 'cargo_weight': Decimal('1500'), 'departure_offset_days': -9, 'arrival_offset_hours': 4},
    {'trip_id': 'T3', 'driver_idx': 2, 'vehicle_idx': 2, 'route_idx': 2, 'status': 'completed', 'cargo_type': 'Food Items', 'cargo_weight': Decimal('5000'), 'departure_offset_days': -8, 'arrival_offset_hours': 4},
    {'trip_id': 'T4', 'driver_idx': 3, 'vehicle_idx': 10, 'route_idx': 3, 'status': 'completed', 'cargo_type': 'Construction Materials', 'cargo_weight': Decimal('8000'), 'departure_offset_days': -7, 'arrival_offset_hours': 3},
    {'trip_id': 'T5', 'driver_idx': 4, 'vehicle_idx': 3, 'route_idx': 4, 'status': 'completed', 'cargo_type': 'Textiles', 'cargo_weight': Decimal('1200'), 'departure_offset_days': -6, 'arrival_offset_hours': 5},
    {'trip_id': 'T6', 'driver_idx': 5, 'vehicle_idx': 4, 'route_idx': 5, 'status': 'completed', 'cargo_type': 'Machinery', 'cargo_weight': Decimal('10000'), 'departure_offset_days': -5, 'arrival_offset_hours': 6},
    {'trip_id': 'T7', 'driver_idx': 6, 'vehicle_idx': 5, 'route_idx': 6, 'status': 'completed', 'cargo_type': 'General Goods', 'cargo_weight': Decimal('3000'), 'departure_offset_days': -4, 'arrival_offset_hours': 4},
    {'trip_id': 'T8', 'driver_idx': 7, 'vehicle_idx': 6, 'route_idx': 7, 'status': 'completed', 'cargo_type': 'Electronics', 'cargo_weight': Decimal('800'), 'departure_offset_days': -3, 'arrival_offset_hours': 2},
    {'trip_id': 'T9', 'driver_idx': 8, 'vehicle_idx': 7, 'route_idx': 8, 'status': 'completed', 'cargo_type': 'Food Items', 'cargo_weight': Decimal('4500'), 'departure_offset_days': -2, 'arrival_offset_hours': 6},
    {'trip_id': 'T10', 'driver_idx': 9, 'vehicle_idx': 8, 'route_idx': 9, 'status': 'completed', 'cargo_type': 'Construction Materials', 'cargo_weight': Decimal('7500'), 'departure_offset_days': -1, 'arrival_offset_hours': 6},
    
    # T11 - T20: In progress trips
    {'trip_id': 'T11', 'driver_idx': 10, 'vehicle_idx': 9, 'route_idx': 10, 'status': 'in_progress', 'cargo_type': 'Textiles', 'cargo_weight': Decimal('2000'), 'departure_offset_days': 0, 'arrival_offset_hours': 2},
    {'trip_id': 'T12', 'driver_idx': 11, 'vehicle_idx': 11, 'route_idx': 11, 'status': 'in_progress', 'cargo_type': 'Machinery', 'cargo_weight': Decimal('6000'), 'departure_offset_days': 0, 'arrival_offset_hours': 2},
    {'trip_id': 'T13', 'driver_idx': 12, 'vehicle_idx': 12, 'route_idx': 0, 'status': 'in_progress', 'cargo_type': 'General Goods', 'cargo_weight': Decimal('3500'), 'departure_offset_days': 0, 'arrival_offset_hours': 3},
    {'trip_id': 'T14', 'driver_idx': 13, 'vehicle_idx': 13, 'route_idx': 1, 'status': 'in_progress', 'cargo_type': 'Electronics', 'cargo_weight': Decimal('1000'), 'departure_offset_days': 0, 'arrival_offset_hours': 4},
    {'trip_id': 'T15', 'driver_idx': 14, 'vehicle_idx': 14, 'route_idx': 2, 'status': 'in_progress', 'cargo_type': 'Food Items', 'cargo_weight': Decimal('4000'), 'departure_offset_days': 0, 'arrival_offset_hours': 4},
    {'trip_id': 'T16', 'driver_idx': 15, 'vehicle_idx': 15, 'route_idx': 3, 'status': 'in_progress', 'cargo_type': 'Construction Materials', 'cargo_weight': Decimal('9000'), 'departure_offset_days': 0, 'arrival_offset_hours': 3},
    {'trip_id': 'T17', 'driver_idx': 16, 'vehicle_idx': 16, 'route_idx': 4, 'status': 'in_progress', 'cargo_type': 'Textiles', 'cargo_weight': Decimal('1800'), 'departure_offset_days': 0, 'arrival_offset_hours': 5},
    {'trip_id': 'T18', 'driver_idx': 17, 'vehicle_idx': 17, 'route_idx': 5, 'status': 'in_progress', 'cargo_type': 'Machinery', 'cargo_weight': Decimal('8500'), 'departure_offset_days': 0, 'arrival_offset_hours': 6},
    {'trip_id': 'T19', 'driver_idx': 18, 'vehicle_idx': 18, 'route_idx': 6, 'status': 'in_progress', 'cargo_type': 'General Goods', 'cargo_weight': Decimal('2800'), 'departure_offset_days': 0, 'arrival_offset_hours': 4},
    {'trip_id': 'T20', 'driver_idx': 19, 'vehicle_idx': 19, 'route_idx': 7, 'status': 'in_progress', 'cargo_type': 'Electronics', 'cargo_weight': Decimal('1200'), 'departure_offset_days': 0, 'arrival_offset_hours': 2},
    
    # T21 - T30: Scheduled trips
    {'trip_id': 'T21', 'driver_idx': 20, 'vehicle_idx': 20, 'route_idx': 8, 'status': 'scheduled', 'cargo_type': 'Food Items', 'cargo_weight': Decimal('5200'), 'departure_offset_days': 1, 'arrival_offset_hours': 6},
    {'trip_id': 'T22', 'driver_idx': 21, 'vehicle_idx': 21, 'route_idx': 9, 'status': 'scheduled', 'cargo_type': 'Construction Materials', 'cargo_weight': Decimal('11000'), 'departure_offset_days': 1, 'arrival_offset_hours': 6},
    {'trip_id': 'T23', 'driver_idx': 22, 'vehicle_idx': 22, 'route_idx': 10, 'status': 'scheduled', 'cargo_type': 'Textiles', 'cargo_weight': Decimal('2200'), 'departure_offset_days': 2, 'arrival_offset_hours': 2},
    {'trip_id': 'T24', 'driver_idx': 23, 'vehicle_idx': 23, 'route_idx': 11, 'status': 'scheduled', 'cargo_type': 'Machinery', 'cargo_weight': Decimal('7000'), 'departure_offset_days': 2, 'arrival_offset_hours': 2},
    {'trip_id': 'T25', 'driver_idx': 24, 'vehicle_idx': 24, 'route_idx': 12, 'status': 'scheduled', 'cargo_type': 'General Goods', 'cargo_weight': Decimal('3800'), 'departure_offset_days': 3, 'arrival_offset_hours': 2},
    {'trip_id': 'T26', 'driver_idx': 25, 'vehicle_idx': 25, 'route_idx': 13, 'status': 'scheduled', 'cargo_type': 'Electronics', 'cargo_weight': Decimal('950'), 'departure_offset_days': 3, 'arrival_offset_hours': 2},
    {'trip_id': 'T27', 'driver_idx': 26, 'vehicle_idx': 26, 'route_idx': 0, 'status': 'scheduled', 'cargo_type': 'Food Items', 'cargo_weight': Decimal('4800'), 'departure_offset_days': 4, 'arrival_offset_hours': 3},
    {'trip_id': 'T28', 'driver_idx': 27, 'vehicle_idx': 27, 'route_idx': 1, 'status': 'scheduled', 'cargo_type': 'Construction Materials', 'cargo_weight': Decimal('9500'), 'departure_offset_days': 4, 'arrival_offset_hours': 4},
    {'trip_id': 'T29', 'driver_idx': 28, 'vehicle_idx': 28, 'route_idx': 2, 'status': 'scheduled', 'cargo_type': 'Textiles', 'cargo_weight': Decimal('1600'), 'departure_offset_days': 5, 'arrival_offset_hours': 4},
    {'trip_id': 'T30', 'driver_idx': 29, 'vehicle_idx': 29, 'route_idx': 3, 'status': 'scheduled', 'cargo_type': 'Machinery', 'cargo_weight': Decimal('7800'), 'departure_offset_days': 5, 'arrival_offset_hours': 3},
]


class Command(BaseCommand):
    help = 'Seeds the database with fleet management data. Edit VEHICLES, DRIVERS, and TRIPS at the top of this file to customize.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding fleet management data...')
        
        # Clear existing data
        FuelRecord.objects.all().delete()
        Maintenance.objects.all().delete()
        Trip.objects.all().delete()
        Driver.objects.all().delete()
        Vehicle.objects.all().delete()
        
        # Create Vehicles
        vehicles = []
        for vdata in VEHICLES:
            vdata['last_service_date'] = timezone.now().date() - timedelta(days=random.randint(10, 60))
            v = Vehicle.objects.create(**vdata)
            vehicles.append(v)
        
        self.stdout.write(f'Created {len(vehicles)} vehicles')
        
        # Create Drivers and assign to vehicles
        drivers = []
        for i, ddata in enumerate(DRIVERS):
            d = Driver.objects.create(**ddata)
            # Assign each driver to the corresponding vehicle (if exists)
            if i < len(vehicles):
                d.assigned_vehicle = vehicles[i]
                d.save()
                vehicles[i].assigned_driver = d
                vehicles[i].save()
            drivers.append(d)
        
        self.stdout.write(f'Created {len(drivers)} drivers')
        
        # Create Trips
        trips = []
        for tdata in TRIPS:
            driver = drivers[tdata['driver_idx']]
            vehicle = vehicles[tdata['vehicle_idx']]
            origin, destination, distance = ROUTES[tdata['route_idx']]
            
            departure = timezone.now() + timedelta(days=tdata['departure_offset_days'])
            arrival = None
            if tdata['status'] in ['completed', 'in_progress']:
                arrival = departure + timedelta(hours=tdata['arrival_offset_hours'])
            
            trip = Trip.objects.create(
                driver=driver,
                vehicle=vehicle,
                origin=origin,
                destination=destination,
                distance=distance,
                departure_date=departure,
                arrival_date=arrival,
                status=tdata['status'],
                cargo_type=tdata['cargo_type'],
                cargo_weight=tdata['cargo_weight'],
                fuel_consumed=Decimal(str(round(distance * 0.3, 2))),
                notes=''
            )
            trips.append(trip)
        
        self.stdout.write(f'Created {len(trips)} trips')
        
        # Create Maintenance Records
        service_types = ['oil_change', 'tire_rotation', 'brake_service', 'engine_repair', 'inspection']
        mechanics = ['AutoCare Garage', 'Goodyear Service', 'Master Motors', 'Quick Fix Workshop']
        
        for i in range(15):
            vehicle = random.choice(vehicles)
            service_date = timezone.now().date() - timedelta(days=random.randint(1, 90))
            status = random.choice(['completed', 'completed', 'scheduled'])
            
            Maintenance.objects.create(
                vehicle=vehicle,
                service_type=random.choice(service_types),
                description=f'Regular {random.choice(service_types).replace("_", " ")} service',
                service_date=service_date,
                completion_date=service_date + timedelta(days=random.randint(1, 3)) if status == 'completed' else None,
                cost=Decimal(str(random.randint(50, 500))),
                mileage_at_service=vehicle.mileage - random.randint(0, 5000),
                mechanic_name=random.choice(mechanics),
                status=status
            )
        
        self.stdout.write('Created 15 maintenance records')
        
        # Create Fuel Records
        stations = ['Shell Kampala', 'Total Entebbe', 'STC Oils', 'Green Fuel', 'City Oil']
        
        for i in range(25):
            vehicle = random.choice(vehicles)
            driver = vehicle.assigned_driver if vehicle.assigned_driver else random.choice(drivers)
            trip = random.choice(trips) if random.random() > 0.3 else None
            
            FuelRecord.objects.create(
                vehicle=vehicle,
                driver=driver,
                trip=trip,
                liters=Decimal(str(round(random.uniform(20, 100), 2))),
                price_per_liter=Decimal('1.45'),
                odometer_reading=vehicle.mileage + random.randint(100, 2000),
                fuel_type='diesel',
                station=random.choice(stations),
                date=timezone.now().date() - timedelta(days=random.randint(0, 60)),
                receipt_number=f'RCP-{random.randint(10000, 99999)}'
            )
        
        self.stdout.write('Created 25 fuel records')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded fleet management data!'))
        self.stdout.write(self.style.SUCCESS('Edit VEHICLES, DRIVERS, and TRIPS in seed_fleet.py to customize your seed data.'))