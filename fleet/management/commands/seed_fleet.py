from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from fleet.models import Vehicle, Driver, Trip, Maintenance, FuelRecord


class Command(BaseCommand):
    help = 'Seeds the database with sample fleet management data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding fleet management data...')
        
        # Clear existing data
        FuelRecord.objects.all().delete()
        Maintenance.objects.all().delete()
        Trip.objects.all().delete()
        Driver.objects.all().delete()
        Vehicle.objects.all().delete()
        
        # Create Vehicles
        vehicles_data = [
            {'vehicle_id': 'VH-001', 'registration_number': 'UAJ 123A', 'vehicle_type': 'truck', 'make': 'Isuzu', 'model': 'NPR', 'year': 2022, 'capacity_tonnes': '5', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 45000},
            {'vehicle_id': 'VH-002', 'registration_number': 'UAJ 124B', 'vehicle_type': 'truck', 'make': 'Hino', 'model': '300', 'year': 2021, 'capacity_tonnes': '10', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 62000},
            {'vehicle_id': 'VH-003', 'registration_number': 'UAJ 125C', 'vehicle_type': 'van', 'make': 'Toyota', 'model': 'Hiace', 'year': 2023, 'capacity_passengers': '12', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 28000},
            {'vehicle_id': 'VH-004', 'registration_number': 'UAJ 126D', 'vehicle_type': 'pickup', 'make': 'Ford', 'model': 'Ranger', 'year': 2022, 'capacity_tonnes': '1', 'status': 'maintenance', 'fuel_type': 'diesel', 'mileage': 38000},
            {'vehicle_id': 'VH-005', 'registration_number': 'UAJ 127E', 'vehicle_type': 'truck', 'make': 'Mitsubishi', 'model': 'Fuso', 'year': 2020, 'capacity_tonnes': '10', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 85000},
            {'vehicle_id': 'VH-006', 'registration_number': 'UAJ 128F', 'vehicle_type': 'bus', 'make': 'Yutong', 'model': 'ZK6105', 'year': 2021, 'capacity_passengers': '40', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 52000},
            {'vehicle_id': 'VH-007', 'registration_number': 'UAJ 129G', 'vehicle_type': 'van', 'make': 'Mercedes-Benz', 'model': 'Sprinter', 'year': 2023, 'capacity_passengers': '12', 'status': 'active', 'fuel_type': 'diesel', 'mileage': 15000},
            {'vehicle_id': 'VH-008', 'registration_number': 'UAJ 130H', 'vehicle_type': 'pickup', 'make': 'Nissan', 'model': 'Navara', 'year': 2022, 'capacity_tonnes': '1', 'status': 'out_of_service', 'fuel_type': 'diesel', 'mileage': 72000},
        ]
        
        vehicles = []
        for vdata in vehicles_data:
            vdata['last_service_date'] = timezone.now().date() - timedelta(days=random.randint(10, 60))
            v = Vehicle.objects.create(**vdata)
            vehicles.append(v)
        
        self.stdout.write(f'Created {len(vehicles)} vehicles')
        
        # Create Drivers
        drivers_data = [
            {'employee_id': 'DRV-001', 'full_name': 'John Musanje', 'license_number': 'DL-2020-4521', 'license_expiry': timezone.now().date() + timedelta(days=730), 'phone_number': '+256 772 123 456', 'email': 'j.musanje@fleeting.co.ug', 'status': 'available', 'total_trips': 145, 'total_distance': 28500, 'rating': Decimal('4.85')},
            {'employee_id': 'DRV-002', 'full_name': 'Sarah Namuli', 'license_number': 'DL-2019-3847', 'license_expiry': timezone.now().date() + timedelta(days=450), 'phone_number': '+256 770 234 567', 'email': 's.namuli@fleeting.co.ug', 'status': 'on_trip', 'total_trips': 198, 'total_distance': 41200, 'rating': Decimal('4.92')},
            {'employee_id': 'DRV-003', 'full_name': 'Peter Ssentongo', 'license_number': 'DL-2021-5623', 'license_expiry': timezone.now().date() + timedelta(days=890), 'phone_number': '+256 773 345 678', 'email': 'p.ssentongo@fleeting.co.ug', 'status': 'available', 'total_trips': 87, 'total_distance': 15800, 'rating': Decimal('4.71')},
            {'employee_id': 'DRV-004', 'full_name': 'Grace Nakato', 'license_number': 'DL-2018-2156', 'license_expiry': timezone.now().date() + timedelta(days=200), 'phone_number': '+256 774 456 789', 'email': 'g.nakato@fleeting.co.ug', 'status': 'on_leave', 'total_trips': 234, 'total_distance': 52000, 'rating': Decimal('4.95')},
            {'employee_id': 'DRV-005', 'full_name': 'Michael Kigozi', 'license_number': 'DL-2022-6789', 'license_expiry': timezone.now().date() + timedelta(days=1100), 'phone_number': '+256 775 567 890', 'email': 'm.kigozi@fleeting.co.ug', 'status': 'available', 'total_trips': 56, 'total_distance': 9800, 'rating': Decimal('4.63')},
            {'employee_id': 'DRV-006', 'full_name': 'Faith Amongi', 'license_number': 'DL-2020-7890', 'license_expiry': timezone.now().date() + timedelta(days=650), 'phone_number': '+256 776 678 901', 'email': 'f.amongi@fleeting.co.ug', 'status': 'on_trip', 'total_trips': 112, 'total_distance': 24500, 'rating': Decimal('4.78')},
        ]
        
        drivers = []
        for i, ddata in enumerate(drivers_data):
            d = Driver.objects.create(**ddata)
            if i < 6 and i < len(vehicles):
                d.assigned_vehicle = vehicles[i]
                d.save()
                vehicles[i].assigned_driver = d
                vehicles[i].save()
            drivers.append(d)
        
        self.stdout.write(f'Created {len(drivers)} drivers')
        
        # Create Trips
        routes = [
            ('Kampala', 'Jinja', 120),
            ('Kampala', 'Entebbe', 40),
            ('Kampala', 'Mbarara', 220),
            ('Kampala', 'Gulu', 340),
            ('Kampala', 'Soroti', 210),
            ('Kampala', 'Kasese', 350),
            ('Kampala', 'Mbale', 230),
            ('Jinja', 'Kampala', 120),
            ('Entebbe', 'Kampala', 40),
            ('Mbarara', 'Kampala', 220),
        ]
        
        statuses = ['completed', 'completed', 'completed', 'in_progress', 'scheduled']
        trips = []
        for i in range(15):
            driver = random.choice(drivers)
            vehicle = random.choice([v for v in vehicles if v.status == 'active'])
            origin, destination, distance = random.choice(routes)
            status = random.choice(statuses)
            
            departure = timezone.now() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 12))
            arrival = None
            if status in ['completed', 'in_progress']:
                arrival = departure + timedelta(hours=distance/60)
            
            trip = Trip.objects.create(
                driver=driver,
                vehicle=vehicle,
                origin=origin,
                destination=destination,
                distance=distance,
                departure_date=departure,
                arrival_date=arrival,
                status=status,
                cargo_type=random.choice(['General Goods', 'Electronics', 'Food Items', 'Construction Materials', 'Textiles']),
                cargo_weight=Decimal(str(random.randint(500, 5000))),
                fuel_consumed=Decimal(str(round(distance * 0.3, 2))),
                notes=''
            )
            trips.append(trip)
        
        self.stdout.write(f'Created {len(trips)} trips')
        
        # Create Maintenance Records
        service_types = ['oil_change', 'tire_rotation', 'brake_service', 'engine_repair', 'inspection']
        mechanics = ['AutoCare Garage', 'Goodyear Service', 'Master Motors', 'Quick Fix Workshop']
        
        for i in range(12):
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
        
        self.stdout.write('Created 12 maintenance records')
        
        # Create Fuel Records
        stations = ['Shell Kampala', 'Total Entebbe', 'STC Oils', 'Green Fuel', 'City Oil']
        
        for i in range(20):
            vehicle = random.choice(vehicles)
            # Find a driver who has driven this vehicle
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
        
        self.stdout.write('Created 20 fuel records')
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded fleet management data!'))