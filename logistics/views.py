from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

# Create your views here.

def home(request):
    return render(request, 'logistics/home.html')

def about(request):
    return render(request, 'logistics/about.html')

def services(request):
    return render(request, 'logistics/services.html')

def booking(request):
    if request.method == 'POST':
        booking = Booking(
            service_type=request.POST.get('service_type'),
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            pickup_location=request.POST.get('pickup_location'),
            destination=request.POST.get('destination'),
            calculated_distance=request.POST.get('calculated_distance', 0),
            estimated_price=request.POST.get('estimated_price', 0),
            currency=request.POST.get('currency', 'USD'),
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

def coverage(request):
    return render(request, 'logistics/coverage.html')
