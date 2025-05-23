import math
import random
from datetime import datetime, timedelta
from typing import Tuple
from config import settings
from models.data_models import Coordinates  # Import hinzugefügt

def haversine_distance(coord1: Coordinates, coord2: Coordinates) -> float:
    """
    Calculate great-circle distance between two points in meters.
    """
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(coord1.lat)
    phi2 = math.radians(coord2.lat)
    delta_phi = math.radians(coord2.lat - coord1.lat)
    delta_lambda = math.radians(coord2.lng - coord1.lng)
    
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def generate_nearby_coords(base: Coordinates, max_dist_m: int) -> Coordinates:
    """
    Generate random coordinates within max_dist_m meters of base.
    """
    while True:
        lat_offset = random.uniform(-max_dist_m / 111000, max_dist_m / 111000)
        lng_offset = random.uniform(-max_dist_m / 75000, max_dist_m / 75000)
        new_coords = Coordinates(
            lat=base.lat + lat_offset,
            lng=base.lng + lng_offset
        )
        if haversine_distance(new_coords, base) <= max_dist_m:
            return new_coords

def generate_residential_coords(area_name: str, area_coords: Tuple[float, float]) -> Tuple[str, Coordinates]:
    """
    Generate random coordinates within a residential area's radius.
    """
    base = Coordinates(lat=area_coords[0], lng=area_coords[1])
    coords = generate_nearby_coords(base, settings.RESIDENTIAL_AREA_RADIUS)
    return area_name, coords

def generate_destination_coords(base_coords: Tuple[float, float]) -> Coordinates:
    """
    Generate random coordinates within destination radius.
    """
    base = Coordinates(dataclass=True, lat=base_coords[0], lng=base_coords[1])
    return generate_nearby_coords(base, settings.DESTINATION_RADIUS)

def get_future_departure_time(time_str: str) -> datetime:
    """
    Convert time string to future datetime with buffer.
    """
    now = datetime.now()
    departure = datetime.strptime(time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    buffer = timedelta(hours=1)
    if departure < now + buffer:
        departure = now + buffer
    return departure.replace(second=0, microsecond=0)