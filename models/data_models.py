from dataclasses import dataclass
from datetime import datetime, time, date
from typing import List, Optional, Tuple
from enum import Enum, auto

class TripType(Enum):
    OUTBOUND = "Hinfahrt"  # To work
    RETURN = "Rückfahrt"   # To home

@dataclass
class Coordinates:
    lat: float
    lng: float

@dataclass
class User:
    id: str
    name: str
    is_driver: bool
    is_rider: bool
    residential_area: Tuple[str, Tuple[float, float]]

    def request_ride(self, start_point: str, end_point: str, start_coords: Coordinates,
                    end_coords: Coordinates, desired_arrival_time: datetime,
                    time_flexibility_min: int) -> Optional['RideRequest']:
        """
        Create a ride request for this user.
        """
        return RideRequest(
            rider=self,
            start_point=start_point,
            end_point=end_point,
            start_coords=start_coords,
            end_coords=end_coords,
            desired_arrival_time=desired_arrival_time,
            time_flexibility_min=time_flexibility_min
        )

@dataclass
class ScheduleRule:
    weekday: int  # 0=Monday, 6=Sunday
    departure_time: time
    trip_type: TripType
    active: bool = True

@dataclass
class WeeklyCommute:
    outbound_rules: List[ScheduleRule]
    return_rules: List[ScheduleRule]
    
    def get_todays_rides(self, template: 'RideTemplate') -> List['Ride']:
        """
        Generate rides for today based on the schedule.
        """
        today_weekday = datetime.now().weekday()
        today_date = datetime.now().date()
        
        rides = []
        for rule in self.outbound_rules:
            if rule.weekday == today_weekday and rule.active:
                rides.append(template.create_ride(
                    departure_time=datetime.combine(today_date, rule.departure_time),
                    trip_type=TripType.OUTBOUND
                ))
        
        for rule in self.return_rules:
            if rule.weekday == today_weekday and rule.active:
                rides.append(template.create_ride(
                    departure_time=datetime.combine(today_date, rule.departure_time),
                    trip_type=TripType.RETURN
                ))
        
        return rides

@dataclass
class RideTemplate:
    driver: User
    outbound_start: str
    outbound_end: str
    return_start: str
    return_end: str
    outbound_start_coords: Coordinates
    outbound_end_coords: Coordinates
    return_start_coords: Coordinates
    return_end_coords: Coordinates
    max_detour_min: int
    available_seats: int
    schedule: WeeklyCommute
    
    def create_ride(self, departure_time: datetime, trip_type: TripType) -> 'Ride':
        """
        Create a ride based on the template and trip type.
        """
        if trip_type == TripType.OUTBOUND:
            return Ride(
                driver=self.driver,
                start_point=self.outbound_start,
                end_point=self.outbound_end,
                start_coords=self.outbound_start_coords,
                end_coords=self.outbound_end_coords,
                departure_time=departure_time,
                max_detour_min=self.max_detour_min,
                available_seats=self.available_seats,
                trip_type=trip_type
            )
        else:
            return Ride(
                driver=self.driver,
                start_point=self.return_start,
                end_point=self.return_end,
                start_coords=self.return_start_coords,
                end_coords=self.return_end_coords,
                departure_time=departure_time,
                max_detour_min=self.max_detour_min,
                available_seats=self.available_seats,
                trip_type=trip_type
            )
    
    def generate_daily_rides(self) -> List['Ride']:
        """
        Generate all rides for today based on the schedule.
        """
        return self.schedule.get_todays_rides(self)

@dataclass
class Ride:
    driver: User
    start_point: str
    end_point: str
    start_coords: Coordinates
    end_coords: Coordinates
    departure_time: datetime
    max_detour_min: int
    available_seats: int
    trip_type: TripType = TripType.OUTBOUND
    route_distance: float = 0.0
    route_duration: float = 0.0
    route_polyline: List[Tuple[float, float]] = None
    matched_riders: List['RideRequest'] = None
    
    def __post_init__(self):
        if self.route_polyline is None:
            self.route_polyline = []
        if self.matched_riders is None:
            self.matched_riders = []

    def remove_rider(self, request: 'RideRequest'):
        """
        Remove a rider from the matched riders list.
        """
        if request in self.matched_riders:
            self.matched_riders.remove(request)

@dataclass
class RideRequest:
    rider: User
    start_point: str
    end_point: str
    start_coords: Coordinates
    end_coords: Coordinates
    desired_arrival_time: datetime
    time_flexibility_min: int
    matched_ride: Optional[Ride] = None
    
    def accept_match(self, ride: Ride):
        """
        Accept a match with a ride.
        """
        self.matched_ride = ride
        ride.matched_riders.append(self)