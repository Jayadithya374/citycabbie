from django.db import models

# Create your models here.
class City(models.Model):
    """
    Represents a city
    id - Primary key
    name - Name of the city
    """
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.name
    
class Road(models.Model):
    """
    Represents a road between two cities
    source - Source city
    destination - Destination city
    duration - Duration of travel in minutes
    """
    city_a = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_a')
    city_b = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_b')
    duration = models.FloatField()
    
    def __str__(self):
        return f'{self.city_a} - {self.city_b} ({self.duration} minutes)'
    
    class Meta:
        unique_together = ('city_a', 'city_b')

class Cab(models.Model):
    """
    Represents a cab
    """
    name = models.CharField(max_length=100)
    price_per_minute = models.FloatField() # Although not recommended since floating point imprecision can cause issues
    image_url = models.CharField(max_length=120)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    """
    Represents a booking
    """
    id = models.AutoField(primary_key=True)
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    source = models.ForeignKey(City, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destination')
    booking_time = models.DateTimeField()
    drop_time = models.DateTimeField()
    booking_fare = models.FloatField()
    email = models.EmailField()
    
    def __str__(self):
        return f'{self.cab} from {self.source} to {self.destination}, from {self.booking_time} to {self.drop_time} for {self.booking_fare} rupees for {self.email}'
    
    class Meta:
        ordering = ['-booking_time']
