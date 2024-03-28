"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Ignoring errors for now
from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('duration', views.calculate_duration, name='calculate-duration'),
    path('fare', views.calculate_fare, name='calculate-fare'),
    path('cabs', views.get_all_cabs, name='get-all-cabs'),
    path('availability', views.is_available, name='availability-for-booking'),
    path('book', views.book_cab, name='book-cab'),
    path('bookings', views.get_bookings, name='get-bookings'),
    path('booking/<int:id>', views.BookingView.as_view(), name='get-booking'),
    path('cities', views.get_all_cities, name='get-all-cities'),
    # path('bookings', views.get_bookings, name='get-bookings'),
]
