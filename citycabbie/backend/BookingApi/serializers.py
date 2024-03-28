from rest_framework import serializers
from .models import Cab

class CabSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128)
    price_per_minute = serializers.FloatField()
    image_url = serializers.CharField(max_length=128)
    class Meta:
        model = Cab
        fields = (
            "name",
            "price_per_minute",
            "image_url",
        )

class BookingSerializer(serializers.ModelSerializer):
    cab = CabSerializer()
    source = serializers.CharField(max_length=128)
    destination = serializers.CharField(max_length=128)
    booking_time = serializers.DateTimeField()
    drop_time = serializers.DateTimeField()
    booking_fare = serializers.FloatField()
    email = serializers.EmailField()
    class Meta:
        model = Cab
        fields = (
            "cab",
            "source",
            "destination",
            "booking_time",
            "drop_time",
            "booking_fare",
            "email",
        )