from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Booking
from datetime import date
import logging

logger = logging.getLogger(__name__)

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


# City distances in km (server-side)
CITY_DISTANCES = {
    'kampala': {'entebbe': 40, 'mbarara': 220, 'gulu': 340, 'jinja': 120, 'soroti': 210, 'kasese': 350},
    'entebbe': {'kampala': 40, 'mbarara': 260, 'gulu': 380, 'jinja': 160, 'soroti': 250, 'kasese': 390},
    'jinja': {'kampala': 120, 'entebbe': 160, 'mbarara': 200, 'gulu': 280, 'soroti': 120, 'kasese': 300},
    'mbarara': {'kampala': 220, 'entebbe': 260, 'jinja': 200, 'gulu': 280, 'soroti': 320, 'kasese': 180},
    'gulu': {'kampala': 340, 'entebbe': 380, 'jinja': 280, 'mbarara': 280, 'soroti': 150, 'kasese': 450},
    'soroti': {'kampala': 210, 'entebbe': 250, 'jinja': 120, 'mbarara': 320, 'gulu': 150, 'kasese': 380},
    'kasese': {'kampala': 350, 'entebbe': 390, 'jinja': 300, 'mbarara': 180, 'gulu': 450, 'soroti': 380}
}

# Pricing constants
BASE_PRICES = {'cargo': 50, 'passenger': 30}
RATE_PER_KM = {'cargo': 0.50, 'passenger': 0.30}
UGX_EXCHANGE_RATE = 3800  # 1 USD = 3800 UGX (can be overridden via UGX_EXCHANGE_RATE env var)


def calculate_distance_server_side(pickup_location, destination):
    """Calculate distance between two locations server-side"""
    from_location = pickup_location.lower().replace(', uganda', '').strip()
    to_location = destination.lower().replace(', uganda', '').strip()
    
    if from_location in CITY_DISTANCES and to_location in CITY_DISTANCES[from_location]:
        return CITY_DISTANCES[from_location][to_location]
    if to_location in CITY_DISTANCES and from_location in CITY_DISTANCES[to_location]:
        return CITY_DISTANCES[to_location][from_location]
    return 50  # Default fallback


def calculate_price_server_side(service_type, distance):
    """Calculate price server-side based on service type and distance"""
    base = BASE_PRICES.get(service_type, 50)
    rate = RATE_PER_KM.get(service_type, 0.50)
    return base + (distance * rate)

# Create your views here.

def home(request):
    return render(request, 'logistics/home.html')

def about(request):
    return render(request, 'logistics/about.html')

def services(request):
    return render(request, 'logistics/services.html')

def booking(request):
    if request.method == 'POST':
        # Server-side validation and price calculation
        service_type = request.POST.get('service_type')
        pickup_location = request.POST.get('pickup_location')
        destination = request.POST.get('destination')
        booking_date = request.POST.get('date')
        
        # Calculate price server-side (ignore client-submitted values)
        calculated_distance = calculate_distance_server_side(pickup_location, destination)
        estimated_price = calculate_price_server_side(service_type, calculated_distance)
        
        # Validate required fields
        if not service_type or not pickup_location or not destination:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('booking')
        
        # Validate service type
        if service_type not in ['cargo', 'passenger']:
            messages.error(request, 'Invalid service type selected.')
            return redirect('booking')
        
        # Validate email format
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('booking')
        
        # Validate date
        if not booking_date:
            messages.error(request, 'Please select a booking date.')
            return redirect('booking')
        
        try:
            from datetime import datetime
            parsed_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
            if parsed_date < date.today():
                messages.error(request, 'Booking date cannot be in the past.')
                return redirect('booking')
        except ValueError:
            messages.error(request, 'Invalid date format.')
            return redirect('booking')
        
        if calculated_distance <= 0 or estimated_price <= 0:
            messages.error(request, 'Invalid pickup or destination location.')
            return redirect('booking')
        
        booking = Booking(
            service_type=sanitize_input(service_type, 20),
            name=sanitize_input(request.POST.get('name'), 100),
            phone=sanitize_input(request.POST.get('phone'), 20),
            email=sanitize_input(email, 100),
            pickup_location=sanitize_input(pickup_location, 200),
            destination=sanitize_input(destination, 200),
            calculated_distance=calculated_distance,
            estimated_price=estimated_price,
            currency=sanitize_input(request.POST.get('currency', 'USD'), 3),
            date=parsed_date,
            message=sanitize_input(request.POST.get('message', ''), 500)
        )
        booking.save()
        
        # Generate tracking number (this is done in model's save method)
        # Send confirmation email
        currency = request.POST.get('currency', 'USD')
        if currency == 'UGX':
            price_display = f"USh {float(booking.estimated_price) * UGX_EXCHANGE_RATE:,.0f}"
        else:
            price_display = f"${booking.estimated_price}"
        
        service = "quote" if request.POST.get('service_type') == 'cargo' else "ride"
        
        # Set success message immediately (before any potential errors)
        messages.success(request, f'Thank you, {booking.name}! Your {service} has been submitted. We will contact you soon.')
        
        # Try to send emails (silently fail if not configured)
        try:
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                send_mail(
                    subject=f'Booking Confirmed - {booking.name}',
                    message=f'''Dear {booking.name},

Thank you for booking with Fleeting Logistics Company Limited!

YOUR BOOKING DETAILS:
- Tracking Number: {booking.tracking_number}
- Service Type: {booking.get_service_type_display()}
- Pickup Location: {booking.pickup_location}
- Destination: {booking.destination}
- Distance: {booking.calculated_distance} km
- Estimated Price: {price_display}
- Date: {booking.date}

TRACK YOUR BOOKING:
Use your tracking number ({booking.tracking_number}) at https://fleeting.onrender.com/track/

We will contact you at {booking.phone} to confirm your booking.

Best regards,
Fleeting Logistics Team
''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    fail_silently=True,
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
                    fail_silently=True,
                )
        except Exception as e:
            logger.error(f'Email sending failed for booking {booking.tracking_number}: {str(e)}')
        
        return redirect('booking')
    
    return render(request, 'logistics/booking.html')

def contact(request):
    if request.method == 'POST':
        name = sanitize_input(request.POST.get('name'), 100)
        email = sanitize_input(request.POST.get('email'), 100)
        subject = sanitize_input(request.POST.get('subject', 'General Inquiry'), 100)
        message_text = sanitize_input(request.POST.get('message'), 500)
        
        # Validate email format
        raw_email = request.POST.get('email', '')
        try:
            validate_email(raw_email)
        except ValidationError:
            messages.error(request, 'Please enter a valid email address.')
            return redirect('contact')
        
        # Send confirmation to user and notification to admin
        # Set success message immediately
        messages.success(request, f'Thank you, {name}! Your message has been sent. We will get back to you at {email} soon.')
        
        try:
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                # Confirmation to customer
                send_mail(
                    subject=f'We received your message - {subject}',
                    message=f'''Dear {name},

Thank you for contacting Fleeting Logistics Company Limited!

We have received your message and will get back to you as soon as possible.

Your Message:
{message_text}

Best regards,
Fleeting Logistics Team
''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                
                # Notification to admin
                send_mail(
                    subject=f'Contact Form: {subject} from {name}',
                    message=f'''NEW CONTACT FORM SUBMISSION!

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message_text}
''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
        except Exception as e:
            logger.error(f'Contact email sending failed: {str(e)}')
        
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
    logger.info("Dashboard view called")
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
                
                # Generate delivery code when status changes to in_transit
                if new_status == 'in_transit' and not booking.delivery_code:
                    import secrets
                    booking.delivery_code = secrets.token_hex(3).upper()
                
                booking.save()
                messages.success(request, f'Booking {booking.tracking_number} updated from {old_status} to {new_status}')
            except Booking.DoesNotExist:
                messages.error(request, 'Booking not found')
    return redirect('dashboard')
