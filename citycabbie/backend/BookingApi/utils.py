from .models import City, Road
import heapq
from django.core.cache import cache
from functools import wraps

def cache_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = f'{func.__name__}_{args}_{kwargs}'
        result = cache.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(cache_key, result, timeout=3600)  # Set expiration time (in seconds)
        return result
    return wrapper

@cache_result
def get_all_cities():
    return City.objects.all()

@cache_result
def get_all_roads():
    return Road.objects.all()

def is_valid_city(city_name):
    return City.objects.filter(name=city_name).exists()

@cache_result
def calculate_duration(source, destination):
    """
    Calculate the duration of travel between two locations
    """
    if not is_valid_city(source) or not is_valid_city(destination):
        raise ValueError('Invalid source or destination')
    
    source_city = City.objects.get(name=source)
    destination_city = City.objects.get(name=destination)
    cities = get_all_cities()
    # For now, we will use Djikstra's algorithm to calculate the duration. 
    val = djikstra(source_city, destination_city, cities, get_all_roads())
    if val is None:
        raise ValueError('No path between the two cities')
    return val

def djikstra(source, destination, cities, roads):
    """
    Djikstra's algorithm to calculate the shortest path between two cities
    I have modularized this function so that it can be easily replaced with a more efficient algorithm in the future
    Also no db queries are made in this function, so it can be easily tested
    """
    edges = {}
    dist = {}
    parent = {}
    parent[source] = None
    queue = []

    for city in cities:
        edges[city] = []
        dist[city] = float('inf')

    for road in roads:
        edges[road.city_a].append((road.duration, road.city_b))
        edges[road.city_b].append((road.duration, road.city_a))
    
    heapq.heappush(queue, (0, source))
    dist[source] = 0

    while queue:
        current_distance, current_city = heapq.heappop(queue)
        if current_city == destination:
            distance = current_distance
            path = []
            while current_city:
                path.append(current_city)
                current_city = parent[current_city]
            return (distance, path[::-1])
        
        if current_distance > dist[current_city]:
            continue
        
        for distance, neighbour in edges[current_city]:
            if dist[neighbour] > dist[current_city] + distance:
                dist[neighbour] = dist[current_city] + distance
                heapq.heappush(queue, (dist[neighbour], neighbour))
                parent[neighbour] = current_city

    # If no path is found
    return None

