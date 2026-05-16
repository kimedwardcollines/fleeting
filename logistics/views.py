from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
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
        
        service = "quote" if request.POST.get('service_type') == 'cargo' else "ride"
        currency = request.POST.get('currency', 'USD')
        if currency == 'UGX':
            price_display = f"USh {float(booking.estimated_price) * 3800:,.0f}"
        else:
            price_display = f"${booking.estimated_price}"
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
