from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg, Q
from datetime import datetime, timedelta
from .models import Vehicle, Driver, Trip, Maintenance, FuelRecord


@login_required
def fleet_dashboard(request):
    """Fleet Management Dashboard"""
    # Vehicle statistics
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    maintenance_vehicles = Vehicle.objects.filter(status='maintenance').count()
    
    # Driver statistics
    total_drivers = Driver.objects.count()
    available_drivers = Driver.objects.filter(status='available').count()
    
    # Trip statistics
    total_trips = Trip.objects.count()
    active_trips = Trip.objects.filter(status='in_progress').count()
    completed_trips = Trip.objects.filter(status='completed').count()
    
    # Fuel cost (this month)
    today = datetime.now()
    month_start = today.replace(day=1)
    monthly_fuel_cost = FuelRecord.objects.filter(
        date__gte=month_start.date()
    ).aggregate(total=Sum('total_cost'))['total'] or 0
    
    # Vehicle status distribution
    vehicle_status = {
        'active': Vehicle.objects.filter(status='active').count(),
        'maintenance': Vehicle.objects.filter(status='maintenance').count(),
        'out_of_service': Vehicle.objects.filter(status='out_of_service').count(),
    }
    
    # Trip status distribution
    trip_status = {
        'scheduled': Trip.objects.filter(status='scheduled').count(),
        'in_progress': Trip.objects.filter(status='in_progress').count(),
        'completed': Trip.objects.filter(status='completed').count(),
        'cancelled': Trip.objects.filter(status='cancelled').count(),
    }
    
    # Monthly fuel costs (last 6 months)
    monthly_fuel = []
    for i in range(5, -1, -1):
        month = today.replace(day=1) - timedelta(days=i * 30)
        month_end = (month + timedelta(days=32)).replace(day=1)
        cost = FuelRecord.objects.filter(
            date__gte=month.date(),
            date__lt=month_end.date()
        ).aggregate(total=Sum('total_cost'))['total'] or 0
        monthly_fuel.append({
            'month': month.strftime('%b'),
            'cost': float(cost)
        })
    
    # Recent trips
    recent_trips = Trip.objects.all()[:5]
    
    # Vehicles needing maintenance (based on time/mileage intervals)
    vehicles_needing_maintenance = []
    for vehicle in Vehicle.objects.filter(status='active'):
        if vehicle.is_maintenance_due():
            vehicles_needing_maintenance.append({
                'vehicle': vehicle,
                'service_type': vehicle.get_recommended_service(),
                'description': vehicle.get_service_description(),
                'days_overdue': vehicle.get_days_since_last_service() - vehicle.service_interval_days if vehicle.get_days_since_last_service() else None,
                'next_service_date': vehicle.get_next_service_date(),
            })
    
    # Upcoming maintenance (scheduled in the system)
    upcoming_maintenance = Maintenance.objects.filter(
        service_date__gte=datetime.now().date(),
        status='scheduled'
    ).order_by('service_date')[:5]
    
    context = {
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles,
        'maintenance_vehicles': maintenance_vehicles,
        'total_drivers': total_drivers,
        'available_drivers': available_drivers,
        'total_trips': total_trips,
        'active_trips': active_trips,
        'completed_trips': completed_trips,
        'monthly_fuel_cost': monthly_fuel_cost,
        'vehicle_status': vehicle_status,
        'trip_status': trip_status,
        'monthly_fuel': monthly_fuel,
        'recent_trips': recent_trips,
        'upcoming_maintenance': upcoming_maintenance,
        'vehicles_needing_maintenance': vehicles_needing_maintenance,
    }
    return render(request, 'fleet/dashboard.html', context)


# ============ Vehicle Views ============

@login_required
def vehicle_list(request):
    """List all vehicles"""
    vehicles = Vehicle.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        vehicles = vehicles.filter(status=status_filter)
    return render(request, 'fleet/vehicles/list.html', {'vehicles': vehicles})


@login_required
def vehicle_add(request):
    """Add new vehicle"""
    if request.method == 'POST':
        from .forms import VehicleForm
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('fleet:vehicle_list')
    else:
        from .forms import VehicleForm
        form = VehicleForm()
    return render(request, 'fleet/vehicles/form.html', {'form': form, 'action': 'Add'})


@login_required
def vehicle_edit(request, pk):
    """Edit vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        from .forms import VehicleForm
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('fleet:vehicle_list')
    else:
        from .forms import VehicleForm
        form = VehicleForm(instance=vehicle)
    return render(request, 'fleet/vehicles/form.html', {'form': form, 'action': 'Edit', 'vehicle': vehicle})


@login_required
def vehicle_delete(request, pk):
    """Delete vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('fleet:vehicle_list')
    return render(request, 'fleet/vehicles/delete.html', {'vehicle': vehicle})


# ============ Driver Views ============

@login_required
def driver_list(request):
    """List all drivers"""
    drivers = Driver.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        drivers = drivers.filter(status=status_filter)
    return render(request, 'fleet/drivers/list.html', {'drivers': drivers})


@login_required
def driver_add(request):
    """Add new driver"""
    if request.method == 'POST':
        from .forms import DriverForm
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver added successfully!')
            return redirect('fleet:driver_list')
    else:
        from .forms import DriverForm
        form = DriverForm()
    return render(request, 'fleet/drivers/form.html', {'form': form, 'action': 'Add'})


@login_required
def driver_edit(request, pk):
    """Edit driver"""
    driver = get_object_or_404(Driver, pk=pk)
    if request.method == 'POST':
        from .forms import DriverForm
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated successfully!')
            return redirect('fleet:driver_list')
    else:
        from .forms import DriverForm
        form = DriverForm(instance=driver)
    return render(request, 'fleet/drivers/form.html', {'form': form, 'action': 'Edit', 'driver': driver})


@login_required
def driver_detail(request, pk):
    """Driver profile page"""
    driver = get_object_or_404(Driver, pk=pk)
    trips = Trip.objects.filter(driver=driver).order_by('-departure_date')[:10]
    fuel_records = FuelRecord.objects.filter(driver=driver).order_by('-date')[:5]
    total_fuel = FuelRecord.objects.filter(driver=driver).aggregate(total=Sum('total_cost'))['total'] or 0
    return render(request, 'fleet/drivers/detail.html', {
        'driver': driver,
        'trips': trips,
        'fuel_records': fuel_records,
        'total_fuel': total_fuel
    })


# ============ Trip Views ============

@login_required
def trip_list(request):
    """List all trips"""
    trips = Trip.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        trips = trips.filter(status=status_filter)
    return render(request, 'fleet/trips/list.html', {'trips': trips})


@login_required
def trip_add(request):
    """Create new trip"""
    if request.method == 'POST':
        from .forms import TripForm
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save()
            # Update driver status
            driver = trip.driver
            if trip.status == 'in_progress':
                driver.status = 'on_trip'
                driver.save()
            messages.success(request, f'Trip {trip.trip_id} created successfully!')
            return redirect('fleet:trip_list')
    else:
        from .forms import TripForm
        form = TripForm()
    return render(request, 'fleet/trips/form.html', {'form': form, 'action': 'Create'})


@login_required
def trip_detail(request, pk):
    """Trip details page"""
    trip = get_object_or_404(Trip, pk=pk)
    fuel_records = FuelRecord.objects.filter(trip=trip)
    return render(request, 'fleet/trips/detail.html', {'trip': trip, 'fuel_records': fuel_records})


@login_required
def trip_edit(request, pk):
    """Edit trip"""
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        from .forms import TripForm
        form = TripForm(request.POST, instance=trip)
        if form.is_valid():
            trip = form.save()
            # Update driver status based on trip status
            driver = trip.driver
            if trip.status == 'in_progress':
                driver.status = 'on_trip'
            elif trip.status == 'completed':
                driver.status = 'available'
                driver.total_trips += 1
                driver.total_distance += trip.distance
            driver.save()
            messages.success(request, f'Trip {trip.trip_id} updated successfully!')
            return redirect('fleet:trip_list')
    else:
        from .forms import TripForm
        form = TripForm(instance=trip)
    return render(request, 'fleet/trips/form.html', {'form': form, 'action': 'Edit', 'trip': trip})


# ============ Maintenance Views ============

@login_required
def maintenance_list(request):
    """List all maintenance records"""
    records = Maintenance.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        records = records.filter(status=status_filter)
    # Separate upcoming and history
    upcoming_maintenance = records.filter(service_date__gte=datetime.now().date())
    maintenance_history = records.filter(service_date__lt=datetime.now().date())
    return render(request, 'fleet/maintenance/list.html', {'upcoming_maintenance': upcoming_maintenance, 'maintenance_history': maintenance_history})


@login_required
def maintenance_add(request):
    """Add maintenance record"""
    from .forms import MaintenanceForm
    
    # Handle pre-filled data from dashboard
    initial_data = {}
    if request.GET.get('vehicle'):
        try:
            vehicle = Vehicle.objects.get(pk=request.GET.get('vehicle'))
            initial_data['vehicle'] = vehicle
            # Auto-recommend service type based on vehicle usage
            if request.GET.get('service_type'):
                initial_data['service_type'] = request.GET.get('service_type')
            initial_data['description'] = vehicle.get_service_description()
        except Vehicle.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            record = form.save()
            # Update vehicle status if maintenance is in progress
            if record.status == 'in_progress':
                vehicle = record.vehicle
                vehicle.status = 'maintenance'
                vehicle.last_service_date = record.service_date
                vehicle.save()
            messages.success(request, 'Maintenance record added successfully!')
            return redirect('fleet:maintenance_list')
    else:
        form = MaintenanceForm(initial=initial_data)
    return render(request, 'fleet/maintenance/form.html', {'form': form, 'action': 'Add'})


# ============ Fuel Views ============

@login_required
def fuel_list(request):
    """List all fuel records"""
    records = FuelRecord.objects.all()
    total_cost = records.aggregate(total=Sum('total_cost'))['total'] or 0
    total_liters = records.aggregate(total=Sum('liters'))['total'] or 0
    return render(request, 'fleet/fuel/list.html', {
        'records': records,
        'total_cost': total_cost,
        'total_liters': total_liters
    })


@login_required
def fuel_add(request):
    """Add fuel record"""
    if request.method == 'POST':
        from .forms import FuelRecordForm
        form = FuelRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            # Update vehicle mileage
            vehicle = record.vehicle
            if record.odometer_reading > vehicle.mileage:
                vehicle.mileage = record.odometer_reading
                vehicle.save()
            messages.success(request, 'Fuel record added successfully!')
            return redirect('fleet:fuel_list')
    else:
        from .forms import FuelRecordForm
        form = FuelRecordForm()
    return render(request, 'fleet/fuel/form.html', {'form': form, 'action': 'Add'})


# ============ Report Views ============

@login_required
def reports(request):
    """Reports dashboard"""
    # Fleet Utilization
    total_vehicles = Vehicle.objects.count()
    active_vehicles = Vehicle.objects.filter(status='active').count()
    utilization_rate = (active_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0
    
    # Driver Performance
    driver_stats = Driver.objects.annotate(
        trip_count=Count('trips'),
        total_dist=Sum('trips__distance', filter=Q(trips__status='completed'))
    ).order_by('-total_dist')[:10]
    
    # Fuel Consumption by vehicle
    fuel_by_vehicle = FuelRecord.objects.values('vehicle__registration_number').annotate(
        total_liters=Sum('liters'),
        total_cost=Sum('total_cost')
    ).order_by('-total_cost')[:10]
    
    # Maintenance costs
    maintenance_costs = Maintenance.objects.filter(status='completed').aggregate(
        total=Sum('cost'),
        avg=Avg('cost')
    )
    
    # Monthly breakdown
    monthly_data = []
    for i in range(5, -1, -1):
        month = datetime.now().replace(day=1) - timedelta(days=i * 30)
        month_end = (month + timedelta(days=32)).replace(day=1)
        trips = Trip.objects.filter(
            departure_date__gte=month,
            departure_date__lt=month_end,
            status='completed'
        ).count()
        fuel = FuelRecord.objects.filter(
            date__gte=month.date(),
            date__lt=month_end.date()
        ).aggregate(total=Sum('total_cost'))['total'] or 0
        maint = Maintenance.objects.filter(
            completion_date__gte=month.date(),
            completion_date__lt=month_end.date(),
            status='completed'
        ).aggregate(total=Sum('cost'))['total'] or 0
        monthly_data.append({
            'month': month.strftime('%b %Y'),
            'trips': trips,
            'fuel': float(fuel),
            'maintenance': float(maint)
        })
    
    return render(request, 'fleet/reports.html', {
        'utilization_rate': utilization_rate,
        'driver_stats': driver_stats,
        'fuel_by_vehicle': fuel_by_vehicle,
        'maintenance_costs': maintenance_costs,
        'monthly_data': monthly_data,
    })