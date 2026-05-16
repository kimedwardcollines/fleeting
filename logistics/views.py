from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'logistics/home.html')

def about(request):
    return render(request, 'logistics/about.html')

def services(request):
    return render(request, 'logistics/services.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'General Inquiry')
        message = request.POST.get('message')
        
        # In a production app, you would save to database or send email
        # For now, we'll just show a success message
        messages.success(request, f'Thank you, {name}! Your message has been sent. We will get back to you at {email} soon.')
        return redirect('contact')
    
    return render(request, 'logistics/contact.html')
