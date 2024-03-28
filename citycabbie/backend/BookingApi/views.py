from django.shortcuts import render
from django.http import JsonResponse
from .utils import calculate_duration as util_calculate_duration
from .models import Cab, Booking, City
from .utils import get_all_cities as util_get_all_cities
from datetime import datetime, timedelta
from .serializers import CabSerializer, BookingSerializer
from django.utils.timezone import make_aware
from django.views import View

# Create your views here.
def calculate_duration(request):
    """
    Calculate the duration of travel between two locations
    Expects the following GET parameters:
    - src: The source location
    - dest: The destination location
    Returns:
    - A JSON response with the following
        - status: The status of the request. Either 'success' or 'error'
        - (if status is 'success')
            - duration: The duration of travel between the two locations
        - (if status is 'error')
            - error: The error message
    """

    source = request.GET.get('src')
    destination = request.GET.get('dest')

    if source is None or destination is None or source == '' or destination == '' or source == destination:
        return JsonResponse({
            'status': 'error',
            'error': 'Please provide valid source and destination. They should not be empty and should be different'
            }, status=400)
    
    try:
        res = util_calculate_duration(source, destination)
        return JsonResponse({
            'status': 'success',
            'duration': res[0],
            'path': [city.name for city in res[1]]
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
    
def get_all_cities(request):
    """
    Get all the cities in the database
    Returns:
    - A JSON response with the following
        - status: The status of the request. Either 'success' or 'error'
        - (if status is 'success')
            - cities: A list of all the cities
        - (if status is 'error')
            - error: The error message
    """
    try:
        cities = util_get_all_cities()
        return JsonResponse({
            'status': 'success',
            'cities': [city.name for city in cities]
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
    
def calculate_fare(request):
    """
    Calculate the fare for a Cab between two locations
    Expects the following GET parameters:
    - src: The source location
    - dest: The destination location
    - cab: The Cab for which to calculate the fare
    Returns:
    - A JSON response with the following
        - status: The status of the request. Either 'success' or 'error'
        - (if status is 'success')
            - fare: The fare for the Cab between the two locations
        - (if status is 'error')
            - error: The error message
    """
    cab_name = request.GET.get('cab')
    src = request.GET.get('src')
    dest = request.GET.get('dest')

    try:
        duration = calculate_duration(src, dest)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
    try:
        cab = Cab.objects.get(name=cab_name)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': 'Cab not found'
        }, status=404)
    
    return JsonResponse({
        'status': 'success',
        'fare': cab.price_per_minute * duration,
    })

def get_all_cabs(request):
    """
    Returns all cabs in json serialized format
    """
    cabs = Cab.objects.all()
    print(cabs)
    return JsonResponse({"cabs" : CabSerializer(cabs, many=True).data})

def bookings_lower_bound(bookings, pickuptime):
    if not bookings or len(bookings) == 0:
        return -1
    pickuptime = make_aware(pickuptime)
    if bookings[0].booking_time > pickuptime:
        return 0
    left = 0
    right = len(bookings)
    while left + 1 < right:
        mid = (left + right) // 2
        if bookings[mid].booking_time < pickuptime:
            left = mid
        else:
            right = mid
    return right
    

def is_available(request):
    cab_name = request.GET.get('cab')
    src = request.GET.get('src')
    dest = request.GET.get('dest')
    pickuptime = datetime.strptime(request.GET.get('pickup_time'), '%Y-%m-%dT%H:%M:%S')
    duration = timedelta(minutes=int(request.GET.get('duration')))
    cab = Cab.objects.get(name=cab_name)
    car_bookings = Booking.objects.filter(cab=cab).order_by('booking_time')
    prev_booking_index = bookings_lower_bound(car_bookings, pickuptime)
    next_booking_index = bookings_lower_bound(car_bookings, pickuptime + duration)

    if prev_booking_index != next_booking_index:
        return JsonResponse({
            'status': 'error',
            'error': 'Cab not available'
        }, status=404)
    
    if prev_booking_index > 0:
        print("prev booking drop time")
        print(car_bookings[prev_booking_index - 1].drop_time + timedelta(minutes=util_calculate_duration(car_bookings[prev_booking_index - 1].source.name, src)))
        print(make_aware(pickuptime))
    if next_booking_index >= 0 and next_booking_index < len(car_bookings):
        print('sdf')
        print(make_aware(pickuptime) + duration + timedelta(minutes=util_calculate_duration(dest, car_bookings[next_booking_index].destination.name)))
        print(car_bookings[next_booking_index].booking_time)

    if prev_booking_index > 0 and car_bookings[prev_booking_index - 1].drop_time + timedelta(minutes=util_calculate_duration(car_bookings[prev_booking_index - 1].source.name, src)) > make_aware(pickuptime):
        return JsonResponse({
            'status': 'error',
            'error': 'Conflict with previous booking and not possible to reach source in pickuptime'
        }, status=404)
    
    if next_booking_index >=0 and next_booking_index < len(car_bookings) and make_aware(pickuptime) + duration + timedelta(minutes=util_calculate_duration(dest, car_bookings[next_booking_index].destination.name)) > car_bookings[next_booking_index].booking_time:
        return JsonResponse({
            'status': 'error',
            'error': "Conflict with next booking and not possible to reach next booking's pickup city in pickuptime"
        }, status=404)
    
    return JsonResponse({
        'status': 'success'
    })

def book_cab(request):
    cab_name = request.GET.get('cab')
    src = City.objects.get(name=request.GET.get('src'))
    dest = City.objects.get(name=request.GET.get('dest'))
    email = request.GET.get('email')
    pickuptime = datetime.strptime(request.GET.get('pickup_time'), '%Y-%m-%dT%H:%M:%S')
    duration = int(request.GET.get('duration'))
    cab = Cab.objects.get(name=cab_name)
    availibility = is_available(request)
    if availibility.status_code != 200:
        return availibility
    fare = cab.price_per_minute * duration
    booking = Booking(cab=cab, source=src, destination=dest, booking_time=make_aware(pickuptime), drop_time=make_aware(pickuptime + timedelta(minutes=duration)), booking_fare=fare, email=email)
    booking.save()
    print(booking)
    return JsonResponse({
        'status': 'success',
        'booking': booking.id
    })
    
def get_bookings(request):
    bookings = Booking.objects.all()
    return JsonResponse({"bookings" : BookingSerializer(bookings, many=True).data})

# Creating a class that handles get and post both for modifying a booking
class BookingView(View):

    def get(self, request, id):
        booking = Booking.objects.get(id=id)
        return JsonResponse({"booking" : BookingSerializer(booking).data})

    def post(self, request, id):
        booking = Booking.objects.get(id=id)
        booking.cab = Cab.objects.get(name=request.GET.get('cab'))
        booking.source = City.objects.get(name=request.GET.get('src'))
        booking.destination = City.objects.get(name=request.GET.get('dest'))
        booking.email = request.GET.get('email')
        booking.booking_time = make_aware(datetime.strptime(request.GET.get('pickup_time'), '%Y-%m-%dT%H:%M:%S'))
        booking.drop_time = make_aware(datetime.strptime(request.GET.get('drop_time'), '%Y-%m-%dT%H:%M:%S'))
        booking.booking_fare = Cab.objects.get(name=request.GET.get('cab')).price_per_minute * (booking.drop_time - booking.booking_time).seconds // 60
        try:
            booking.save()
        except Exception as e:
            return JsonResponse({"status" : "error", "error" : str(e)})
        finally:
            return JsonResponse({"status" : "success"})

    def delete(self, request, id):
        booking = Booking.objects.get(id=id)
        booking.delete()
        return JsonResponse({"status" : "success"})