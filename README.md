🚗 Carpool
Carpool is a Python-based ride-sharing application that connects drivers and passengers for efficient, eco-friendly commuting in the Stuttgart area. Powered by the Google Maps Directions API and visualized with Folium maps in a sleek PyQt5 interface, it matches riders with drivers while minimizing detours and optimizing routes. 🌍

✨ Features

Route Calculation 🛣️: Uses Google Maps API to compute precise distances, durations, and route paths.
Smart Matching 🤝: Pairs drivers and riders based on configurable detour (up to 30 min) and time flexibility settings.
Interactive Maps 🗺️: Displays routes and rider locations with Folium, rendered in a PyQt5 GUI.
Stuttgart Scenario 🏙️: Simulates 50 users with realistic routes (e.g., to Mercedes Werk or Stihl Werk 2).
Secure Configuration 🔒: Stores sensitive data like API keys in a .env file, keeping credentials safe.
Modular Design 🧩: Organized into configuration, data models, services, UI, and utility modules for easy maintenance.


📁 Project Structure
Carpool/
├── .env                    # Google Maps API key
├── main.py                 # Application entry point
├── config/
│   └── settings.py         # Configuration and environment variable loading
├── utils/
│   └── helpers.py         # Utility functions (e.g., haversine distance)
├── services/
│   └── routing.py         # Google Maps API integration
├── models/
│   └── data_models.py     # Data classes for rides, riders, and schedules
├── ui/
│   ├── main_window.py     # PyQt5 GUI implementation
│   └── widgets.py        # Custom UI components
├── tests/
│   └── test_helpers.py    # Unit tests for helper functions
├── .gitignore             # Ignored files (e.g., __pycache__, .env)
└── README.md              # You're reading it!


🚀 Getting Started
✅ Prerequisites

Python 3.9+ 🐍
Anaconda or Miniconda (recommended for dependency management)
Google Maps API Key with Directions API enabled
Microsoft Visual C++ Redistributable (2015-2022, x64) for PyQt5 WebEngine

📦 Installation

Clone the Repository:
git clone https://github.com/fakhrialimin/Carpool.git
cd Carpool


Create and Activate a Conda Environment:
conda create -n carpool python=3.9
conda activate carpool


Install Dependencies:
conda install pyqt5 pyqtwebengine googlemaps folium python-dotenv

Alternatively, use pip:
pip install PyQt5 PyQtWebEngine googlemaps folium python-dotenv


Configure the Google Maps API Key:

Create a .env file in the project root (Carpool/) with:GMAPS_API_KEY=your_google_maps_api_key_here


Get a key from the Google Cloud Console:
Create a project.
Enable the Directions API.
Generate an API key under Credentials.




Install Microsoft Visual C++ Redistributable:

Download and install the Visual C++ Redistributable (x64) to support PyQt5’s WebEngine.


Verify Setup:

Test the environment and API key:python test_env.py

Expected output:INFO:__main__:Successfully loaded .env file from C:\path\to\Carpool\.env
INFO:__main__:GMAPS_API_KEY: AIzaSyCdee... (hidden for security)






🏁 Usage

Run the Application:
conda activate carpool
python main.py

On Windows, if using the full Conda path:
& C:/Users/OMAR/anaconda3/envs/carpool/python.exe "C:/Users/OMAR/Documents/Final version of the project/main.py"


Explore the Stuttgart Scenario:

The app launches with a simulated scenario of 50 users (25 drivers, 25 riders) in Stuttgart.
The GUI shows:
A list of rides with details (e.g., driver name, start/end points, available seats).
An interactive Folium map displaying routes and rider markers.
Filters for trip type (outbound/return) and available seats.




Example Interaction:

Select a ride (e.g., “Mohamed Ben Ammar, Hinfahrt, 7:30”) from the ride list.
View matched riders (e.g., “Fatma Trabelsi, Score: 0.95”).
Add/remove riders using the buttons.
See the route visualized on the map with green (start) and red (end) markers.

Example map output:
<div style="font-family: Arial;">
    <h3>Route: Böblingen → Mercedes Werk</h3>
    <!-- Folium map with route polyline and markers -->
</div>




🧪 Running Tests
Run unit tests to verify helper functions (e.g., haversine distance):
conda activate carpool
python -m unittest discover tests

Example test output:
test_haversine_distance (test_helpers.TestHelpers) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK


⚙️ Configuration
Customize settings in config/settings.py:
class Settings:
    def __init__(self):
        self.GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
        self.RESIDENTIAL_AREA_RADIUS = 10_000  # 10 km
        self.DESTINATION_RADIUS = 2_000        # 2 km
        self.MAX_DETOUR_MIN = 30               # minutes
        self.TIME_FLEXIBILITY_MIN = 30         # minutes


Adjust RESIDENTIAL_AREA_RADIUS or DESTINATION_RADIUS for larger/smaller matching areas.
Modify MAX_DETOUR_MIN or TIME_FLEXIBILITY_MIN for stricter/looser matching.


🙋‍♂️ Contributing
We’d love your contributions! 🚀

Fork the repository.
Create a feature branch (git checkout -b feature/your-awesome-feature).
Commit your changes (git commit -m "Add awesome feature").
Push to your branch (git push origin feature/your-awesome-feature).
Open a pull request on GitHub.

See CONTRIBUTING.md (if available) for more details.


🎉 Acknowledgments

Google Maps API 🗺️ for powering route calculations.
Folium 📍 for beautiful interactive maps.
PyQt5 🖼️ for the sleek GUI framework.
python-dotenv 🔑 for secure configuration management.
Built with ❤️ by fakhrialimin.


📬 Contact
Got questions or ideas? Reach out:

GitHub: fakhrialimin


💡 Tip: If you encounter errors (e.g., missing DLLs or API key issues), check the console logs and ensure all dependencies are installed. Run conda list to verify packages and install the Visual C++ Redistributable for PyQt5 compatibility.
