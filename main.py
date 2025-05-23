import random
import uuid
from datetime import datetime, time, timedelta
from typing import List, Tuple
from models.data_models import (
    User, Coordinates, Ride, RideRequest, 
    RideTemplate, WeeklyCommute, ScheduleRule, TripType
)
from utils.helpers import (
    haversine_distance, generate_residential_coords,
    generate_destination_coords, get_future_departure_time
)
from services.routing import calculate_route
from ui.main_window import CarpoolWindow
from PyQt5.QtWidgets import QApplication
import sys

def test_stuttgart_roundtrip_scenario():
    """
    Generate a test scenario for Stuttgart carpooling.
    """
    print("Stuttgart Round-Trip Scenario (50 Persons)...")
    
    if not first_names or not last_names:
        raise ValueError("Name lists cannot be empty")
    if len(residential_areas) < 1 or len(workplaces) < 1:
        raise ValueError("At least one residential area and workplace must be defined")
    
    stuttgart_center = (48.7758, 9.1829)
    mercedes_unterturkheim = (48.7833, 9.2250)
    stihl_werk2 = (48.8316, 9.3100)
    
    residential_areas = [
        ("Böblingen", (48.6833, 9.0167)),
        ("Stuttgart West", (48.7500, 9.1500)),
        ("Schwäbisch Gmünd", (48.8000, 9.8000)),
        ("Ludwigsburg", (48.8973, 9.1922)),
        ("Esslingen", (48.7400, 9.3000)),
        ("Waiblingen", (48.8316, 9.3167)),
        ("Sindelfingen", (48.7000, 9.0167)),
        ("Leonberg", (48.8000, 9.0167)),
        ("Fellbach", (48.8167, 9.2833)),
        ("Backnang", (48.9472, 9.4306)),
        ("Herrenberg", (48.5951, 8.8662)),
        ("Pforzheim", (48.8913, 8.6989)),
        ("Reutlingen", (48.4912, 9.2113)),
        ("Tübingen", (48.5200, 9.0500)),
        ("Aalen", (48.8378, 10.0933)),
        ("Heidenheim", (48.6778, 10.1516)),
        ("Göppingen", (48.7035, 9.6538)),
        ("Nürtingen", (48.6257, 9.3420)),
        ("Kirchheim unter Teck", (48.6468, 9.4538)),
        ("Schorndorf", (48.8054, 9.5272))
    ]
    
    workplaces = [
        ("Mercedes Werk Untertürkheim", mercedes_unterturkheim),
        ("Stihl Werk 2, Waiblingen", stihl_werk2)
    ]

    first_names = [
        "Mohamed", "Fatma", "Ali", "Mariem", "Ahmed", "Amina", "Mahmoud", "Houda", "Youssef", "Samira",
        "Hassan", "Nadia", "Omar", "Leila", "Khalil", "Salwa", "Adel", "Amira", "Tarek", "Rania",
        "Bassem", "Sana", "Wassim", "Yosra", "Nabil", "Hajer", "Karim", "Soumaya", "Fares", "Manel"
    ]

    last_names = [
        "Ben Ammar", "Trabelsi", "Bouzid", "Chaabane", "Gharbi", 
        "Haddad", "Jlassi", "Karray", "Mansouri", "Nasri",
        "Ouertani", "Saadi", "Zaoui", "Abid", "Cherif",
        "Dridi", "Essid", "Fersi", "Ghanmi", "Hamdi",
        "Khalifa", "Laroussi", "Maalej", "Najar", "Rebai",
        "Sassi", "Tlili", "Zoghlami", "Baccar", "Dhieb"
    ]
        
    random.shuffle(first_names)
    random.shuffle(last_names)
    
    users = []
    for i in range(50):
        first = first_names[i % len(first_names)]
        last = last_names[i % len(last_names)]
        name = f"{first} {last}"
        is_driver = i < 25
        residential_area = random.choice(residential_areas)
        users.append(User(
            id=str(uuid.uuid4()),
            name=name,
            is_driver=is_driver,
            is_rider=not is_driver,
            residential_area=residential_area
        ))

    templates = []
    for driver in users[:25]:
        area_name, area_coords = driver.residential_area
        workplace_name, workplace_coords = random.choice(workplaces)
        
        home_coords = generate_residential_coords(area_name, area_coords)[1]
        work_coords = generate_destination_coords(workplace_coords)
        
        schedule = WeeklyCommute(
            outbound_rules=[
                ScheduleRule(weekday=i, departure_time=time(7, 30), trip_type=TripType.OUTBOUND)
                for i in range(5)
            ],
            return_rules=[
                ScheduleRule(weekday=i, departure_time=time(16, 30), trip_type=TripType.RETURN)
                for i in range(5)
            ]
        )
        
        template = RideTemplate(
            driver=driver,
            outbound_start=area_name,
            outbound_end=workplace_name,
            return_start=workplace_name,
            return_end=area_name,
            outbound_start_coords=home_coords,
            outbound_end_coords=work_coords,
            return_start_coords=work_coords,
            return_end_coords=home_coords,
            max_detour_min=random.randint(15, 30),
            available_seats=random.randint(2, 4),
            schedule=schedule
        )
        templates.append(template)

    today_rides = []
    for template in templates:
        today_rides.extend(template.generate_daily_rides())
    
    valid_rides = []
    for ride in today_rides:
        if calculate_route(ride):
            valid_rides.append(ride)

    ride_requests = []
    for rider in users[25:]:
        area_name, area_coords = rider.residential_area
        workplace_name, workplace_coords = random.choice(workplaces)
        
        home_coords = generate_residential_coords(area_name, area_coords)[1]
        work_coords = generate_destination_coords(workplace_coords)
        
        for trip_type in [TripType.OUTBOUND, TripType.RETURN]:
            start_point = area_name if trip_type == TripType.OUTBOUND else workplace_name
            end_point = workplace_name if trip_type == TripType.OUTBOUND else area_name
            start_coords = home_coords if trip_type == TripType.OUTBOUND else work_coords
            end_coords = work_coords if trip_type == TripType.OUTBOUND else home_coords
            
            minutes = random.randint(0, 120)
            arrival_time = get_future_departure_time(
                f"{7 if trip_type == TripType.OUTBOUND else 16 + minutes // 60}:{minutes % 60:02d}"
            )
            
            request = rider.request_ride(
                start_point=start_point,
                end_point=end_point,
                start_coords=start_coords,
                end_coords=end_coords,
                desired_arrival_time=arrival_time,
                time_flexibility_min=random.randint(30, 60)
            )
            if request:
                ride_requests.append(request)

    print(f"\nGenerated {len(valid_rides)} valid rides (outbound and return)")
    print(f"Generated {len(ride_requests)} ride requests")
    
    return valid_rides, ride_requests

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rides, requests = test_stuttgart_roundtrip_scenario()
    window = CarpoolWindow(rides, requests)
    window.show()
    sys.exit(app.exec_())