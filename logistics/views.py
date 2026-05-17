from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.urls import reverse
from .models import Booking

def sanitize_input(value, max_length=200):
    """Sanitize user input by stripping HTML and limiting length"""
    if value:
        # Remove HTML tags
        value = strip_tags(value)
        # Strip whitespace
        value = value.strip()
        # Limit length
        if max_length:
            value = value[:max_length]
        return value
    return ''

# Create your views here.

def home(request):
    return render(request, 'logistics/home.html')

def about(request):
    return render(request, 'logistics/about.html')

def services(request):
    return render(request, 'logistics/services.html')

def booking(request):
    if request.method == 'POST':
        # Server-side validation
        service_type = request.POST.get('service_type')
        
        try:
            calculated_distance = int(request.POST.get('calculated_distance', '0').strip() or '0')
            estimated_price = float(request.POST.get('estimated_price', '0').strip() or '0')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid price or distance calculation.')
            return redirect('booking')
        
        # Validate required fields
        if not service_type or calculated_distance <= 0 or estimated_price <= 0:
            messages.error(request, 'Please calculate the price by entering pickup and destination locations.')
            return redirect('booking')
        
        booking = Booking(
            service_type=sanitize_input(service_type, 20),
            name=sanitize_input(request.POST.get('name'), 100),
            phone=sanitize_input(request.POST.get('phone'), 20),
            email=sanitize_input(request.POST.get('email'), 100),
            pickup_location=sanitize_input(request.POST.get('pickup_location'), 200),
            destination=sanitize_input(request.POST.get('destination'), 200),
            calculated_distance=int(calculated_distance),
            estimated_price=float(estimated_price),
            currency=sanitize_input(request.POST.get('currency'), 3),
            date=request.POST.get('date'),
            message=request.POST.get('message', '')
        )
        booking.save()
        
        # Send confirmation email
        currency = request.POST.get('currency', 'USD')
        if currency == 'UGX':
            price_display = f"USh {float(booking.estimated_price) * 3800:,.0f}"
        else:
            price_display = f"${booking.estimated_price}"
        
        service = "quote" if request.POST.get('service_type') == 'cargo' else "ride"
        
        try:
            send_mail(
                subject=f'Booking Confirmation - {booking.name}',
                message=f'''Dear {booking.name},

Thank you for booking with Fleeting Logistics Company Limited!

BOOKING DETAILS:
- Service Type: {booking.get_service_type_display()}
- Pickup Location: {booking.pickup_location}
- Destination: {booking.destination}
- Distance: {booking.calculated_distance} km
- Estimated Price: {price_display}
- Date: {booking.date}

We will contact you at {booking.phone} to confirm your booking.

Best regards,
Fleeting Logistics Team
''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )
            
            # Send notification to admin
            send_mail(
                subject=f'New Booking: {booking.get_service_type_display()} from {booking.name}',
                message=f'''NEW BOOKING RECEIVED!

Customer: {booking.name}
Phone: {booking.phone}
Email: {booking.email}
Service: {booking.get_service_type_display()}
Pickup: {booking.pickup_location}
Destination: {booking.destination}
Distance: {booking.calculated_distance} km
Price: {price_display}
Date: {booking.date}

Tracking: {booking.tracking_number}

Message: {booking.message}
''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, f'Thank you, {booking.name}! Your {service} has been submitted. A confirmation email has been sent to {booking.email}')
        except:
            messages.success(request, f'Thank you, {booking.name}! Your {service} request has been submitted. Estimated price: {price_display}. We will contact you soon.')
        
        return redirect('booking')
    
    return render(request, 'logistics/booking.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message')
        
        messages.success(request, f'Thank you, {name}! Your message has been sent. We will get back to you at {email} soon.')
        return redirect('contact')
    
    return render(request, 'logistics/contact.html')

def track(request):
    tracking_number = request.GET.get('tracking_number', '').strip().upper()
    booking = None
    error = None
    
    if tracking_number:
        try:
            booking = Booking.objects.get(tracking_number=tracking_number)
        except Booking.DoesNotExist:
            error = "No booking found with this tracking number."
    
    return render(request, 'logistics/track.html', {
        'booking': booking,
        'error': error,
        'tracking_number': tracking_number
    })

def faq(request):
    return render(request, 'logistics/faq.html')

def terms(request):
    return render(request, 'logistics/terms.html')

def privacy(request):
    return render(request, 'logistics/privacy.html')

def verify_delivery(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        tracking = request.POST.get('tracking', '').strip().upper()
        
        try:
            booking = Booking.objects.get(tracking_number=tracking, delivery_code=code)
            if not booking.delivery_verified:
                booking.delivery_verified = True
                booking.status = 'delivered'
                booking.save()
                messages.success(request, f'Delivery verified successfully! Item delivered to {booking.destination}.')
            else:
                messages.info(request, 'This delivery has already been verified.')
        except Booking.DoesNotExist:
            messages.error(request, 'Invalid tracking number or delivery code.')
    
    return render(request, 'logistics/verify_delivery.html')

def coverage(request):
    return render(request, 'logistics/coverage.html')

@login_required
def dashboard(request):
    total_bookings = Booking.objects.count()
    pending_count = Booking.objects.filter(status='pending').count()
    confirmed_count = Booking.objects.filter(status='confirmed').count()
    in_transit_count = Booking.objects.filter(status='in_transit').count()
    delivered_count = Booking.objects.filter(status='delivered').count()
    recent_bookings = Booking.objects.order_by('-created_at')[:10]
    
    return render(request, 'logistics/dashboard.html', {
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'in_transit_count': in_transit_count,
        'delivered_count': delivered_count,
        'recent_bookings': recent_bookings,
    })

@login_required
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'in_transit', 'delivered']:
            try:
                booking = Booking.objects.get(id=booking_id)
                old_status = booking.status
                booking.status = new_status
                booking.save()
                messages.success(request, f'Booking {booking.tracking_number} updated from {old_status} to {new_status}')
            except Booking.DoesNotExist:
                messages.error(request, 'Booking not found')
    return redirect('dashboard')
