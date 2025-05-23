from typing import Optional, Tuple, List
from datetime import datetime
import googlemaps
from googlemaps.exceptions import ApiError, TransportError
from googlemaps.directions import directions

from config.settings import settings
from models.data_models import Coordinates

def calculate_route(
    origin: Coordinates,
    destination: Coordinates,
    departure_time: datetime
) -> Optional[Tuple[float, float, List[Coordinates]]]:
    """
    Calculate the driving route between two coordinates using Google Maps Directions API.
    Returns a tuple containing:
        - Distance in meters
        - Duration in seconds
        - List of Coordinates along the route (from polyline steps)
    """
    try:
        # Initialize the Google Maps client
        gmaps = googlemaps.Client(key=settings.GMAPS_API_KEY)

        # Request directions
        route = directions(
            client=gmaps,
            origin=(origin.lat, origin.lng),
            destination=(destination.lat, destination.lng),
            mode="driving",
            departure_time=departure_time
        )

        if not route or "legs" not in route[0]:
            return None

        leg = route[0]["legs"][0]
        distance = leg["distance"]["value"]  # in meters
        duration = leg["duration"]["value"]  # in seconds

        # Extract polyline coordinates from each step
        polyline: List[Coordinates] = [
            Coordinates(lat=step["start_location"]["lat"], lng=step["start_location"]["lng"])
            for step in leg["steps"]
        ]
        polyline.append(Coordinates(lat=leg["end_location"]["lat"], lng=leg["end_location"]["lng"]))

        return distance, duration, polyline

    except (ApiError, TransportError) as e:
        print(f"Google Maps error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None
 