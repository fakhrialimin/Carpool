from typing import List, Dict, Optional, Tuple
from models.data_models import Ride, RideRequest, Coordinates
from utils.helpers import haversine_distance
from services.routing import gmaps
from googlemaps.directions import directions
from datetime import timedelta

def compute_matches(rides: List[Ride], requests: List[RideRequest]) -> Dict:
    """
    Generate matching matrix between rides and requests.
    """
    matches = {}
    
    for ride in rides:
        if len(ride.matched_riders) >= ride.available_seats:
            continue
            
        rider_matches = []
        for request in requests:
            if request.matched_ride:
                continue
                
            # Calculate detour impact
            new_polyline, new_distance, new_duration = calculate_detour(ride, request)
            if not new_polyline:
                continue
                
            # Check time constraints
            if not check_time_constraints(ride, request, new_duration):
                continue
                
            # Calculate match score
            score = calculate_match_score(ride, request, new_distance, new_duration)
            rider_matches.append({
                'request': request,
                'score': score,
                'details': {
                    'detour_time': new_duration - ride.route_duration,
                    'distance_increase': new_distance - ride.route_distance
                }
            })
            
        if rider_matches:
            matches[ride.driver.name] = sorted(
                rider_matches, 
                key=lambda x: x['score'], 
                reverse=True
            )
    
    return matches

def calculate_detour(ride: Ride, request: RideRequest) -> Tuple[Optional[List[Tuple[float, float]]], float, float]:
    """
    Calculate route with rider pickup and dropoff added.
    """
    try:
        waypoints = [
            (request.start_coords.lat, request.start_coords.lng),
            (request.end_coords.lat, request.end_coords.lng)
        ]
        
        result = directions(
            client=gmaps,
            origin=(ride.start_coords.lat, ride.start_coords.lng),
            destination=(ride.end_coords.lat, ride.end_coords.lng),
            waypoints=waypoints,
            optimize_waypoints=True,
            departure_time=ride.departure_time,
            mode="driving"
        )
        
        if not result:
            return None, 0, 0
            
        leg = result[0]['legs'][0]
        new_distance = leg['distance']['value'] / 1000
        new_duration = leg['duration']['value'] / 60
        
        polyline_points = []
        for step in leg['steps']:
            polyline_points.extend(
                googlemaps.convert.decode_polyline(step['polyline']['points'])
            )
        
        return [(point['lat'], point['lng']) for point in polyline_points], new_distance, new_duration
        
    except Exception as e:
        print(f"Detour calculation error: {e}")
        return None, 0, 0

def check_time_constraints(ride: Ride, request: RideRequest, new_duration: float) -> bool:
    """
    Verify if the new route duration fits within time constraints.
    """
    driver_arrival = ride.departure_time + timedelta(minutes=new_duration)
    min_arrival = request.desired_arrival_time - timedelta(minutes=request.time_flexibility_min)
    max_arrival = request.desired_arrival_time + timedelta(minutes=request.time_flexibility_min)
    return min_arrival <= driver_arrival <= max_arrival

def calculate_match_score(ride: Ride, request: RideRequest, new_distance: float, new_duration: float) -> float:
    """
    Calculate a match score between 0 and 1 based on detour time and distance.
    """
    detour_time = new_duration - ride.route_duration
    distance_ratio = (new_distance / ride.route_distance - 1) if ride.route_distance > 0 else 0
    time_ratio = detour_time / ride.max_detour_min
    
    return max(0, 1 - (time_ratio * 0.4) - (distance_ratio * 0.4))