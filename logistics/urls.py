from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('track/', views.track, name='track'),
    path('coverage/', views.coverage, name='coverage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-booking/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]