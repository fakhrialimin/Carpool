import googlemaps
from config.settings import settings

gmaps = googlemaps.Client(key=settings.GMAPS_API_KEY)
try:
    result = gmaps.directions(
        origin=(48.7758, 9.1829),  # Stuttgart center
        destination=(48.7833, 9.2250),  # Mercedes Werk
        mode="driving"
    )
    print("API key is valid. Route found:", result[0]["legs"][0]["distance"])
except Exception as e:
    print(f"API key test failed: {e}")