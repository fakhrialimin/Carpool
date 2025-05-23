import os
from pathlib import Path
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei im Projektstammverzeichnis
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

class Settings:
    def __init__(self):
        self.GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
        self.RESIDENTIAL_AREA_RADIUS = 10_000  # in meters (10 km)
        self.DESTINATION_RADIUS = 2_000        # in meters (2 km)
        self.MAX_DETOUR_MIN = 30               # in minutes
        self.TIME_FLEXIBILITY_MIN = 30         # in minutes

        self._validate()

    def _validate(self):
        if not self.GMAPS_API_KEY:
            raise ValueError("Environment variable 'GMAPS_API_KEY' is missing. Please check your .env file.")

# Erstelle ein Singleton-Settings-Objekt
settings = Settings()

