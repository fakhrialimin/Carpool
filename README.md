## 🚗 **Carpool**

**Carpool** is a **Python-based ride-sharing app** that connects **drivers** and **passengers** for **efficient**, **eco-friendly commuting** in Stuttgart. Powered by the **Google Maps Directions API** and visualized with **Folium maps** in a sleek **PyQt5 GUI**, it matches riders with drivers while **minimizing detours** and optimizing routes. 🌍

---

## ✨ **Features**

- 🛣️ **Route Calculation**: Uses **Google Maps API** to compute **precise distances**, **durations**, and **route paths**.
- 🤝 **Smart Matching**: Pairs drivers and riders with configurable **detour limits** (up to **30 min**) and **time flexibility**.
- 🗺️ **Interactive Maps**: Displays routes and rider locations with **Folium**, rendered in a **PyQt5 GUI**.
- 🏙️ **Stuttgart Scenario**: Simulates **50 users** (25 drivers, 25 riders) with routes to places like **Mercedes Werk**.
- 🔒 **Secure Configuration**: Stores **API keys** in a `.env` file, keeping credentials safe.
- 🧩 **Modular Design**: Organized into **configuration**, **data models**, **services**, **UI**, and **utility modules**.

---

## 📁 **Project Structure**
Carpool/
├── .env                    # Google Maps API key
├── main.py                 # Application entry point
├── config/
│   └── settings.py         # Configuration and env variable loading
├── utils/
│   └── helpers.py         # Utility functions (e.g., haversine distance)
├── services/
│   └── routing.py         # Google Maps API integration
├── models/
│   └── data_models.py     # Data classes for rides, riders, schedules
├── ui/
│   ├── main_window.py     # PyQt5 GUI implementation
│   └── widgets.py        # Custom UI components
├── tests/
│   └── test_helpers.py    # Unit tests for helper functions
├── .gitignore             # Ignored files (e.g., pycache, .env)
└── README.md              # This file



---

## 🚀 **Getting Started**

### ✅ **Prerequisites**

- 🐍 **Python 3.9+**
- **Anaconda** or **Miniconda** (recommended)
- 🔑 **Google Maps API Key** with **Directions API** enabled
- **Microsoft Visual C++ Redistributable (2015-2022, x64)** for PyQt5 WebEngine

### 📦 **Installation**

1. **Navigate to Project Directory**:
   ```
   cd "C:\Users\OMAR\Documents\Final version of the project"
Create and Activate Conda Environment:

conda create -n carpool python=3.9
conda activate carpool
Install Dependencies:

conda install pyqt5 pyqtwebengine googlemaps folium python-dotenv
Configure Google Maps API Key:
Create a .env file in C:\Users\OMAR\Documents\Final version of the project with:

GMAPS_API_KEY=your_google_maps_api_key_here
Get a key from the Google Cloud Console:
Create a project.
Enable Directions API.
Generate an API key under Credentials.
Install Visual C++ Redistributable:
Download and install the Visual C++ Redistributable (x64) for PyQt5 WebEngine support.
Verify Setup:
Test the environment and API key:

python test_env.py
Expected Output:

INFO:__main__:Successfully loaded .env file from C:\Users\OMAR\Documents\Final version of the project\.env
INFO:__main__:GMAPS_API_KEY: AIzaSyCdee... (hidden for security)

🏁 Usage
Run the Application:


conda activate carpool
python main.py
Or use the full path:


& C:/Users/OMAR/anaconda3/envs/carpool/python.exe "C:/Users/OMAR/Documents/Final version of the project/main.py"
Explore Stuttgart Scenario:

The app launches with a simulated scenario of 50 users (25 drivers, 25 riders).
The GUI shows:
A list of rides (e.g., driver name, start/end points, seats).
An interactive Folium map with routes and rider markers.
Filters for trip type (outbound/return) and seats.
Example Interaction:

Select a ride (e.g., “Mohamed Ben Ammar, Hinfahrt, 7:30”).
View matched riders (e.g., “Fatma Trabelsi, Score: 0.95”).
Add/remove riders via buttons.
See the route on the map with green (start) and red (end) markers.

Example Map Output:

<div style="font-family: Arial;">
    <h3>Route: Böblingen → Mercedes Werk</h3>
    <!-- Folium map with route polyline and markers -->
</div>

🧪 Running Tests
Run unit tests for helper functions (e.g., haversine distance):


conda activate carpool
python -m unittest discover tests
Example Output:


test_haversine_distance (test_helpers.TestHelpers) ... ok
----------------------------------------------------------------------
Ran 1 test in 0.001s
OK
⚙️ Configuration
Customize settings in config/settings.py:


class Settings:
    def __init__(self):
        self.GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
        self.RESIDENTIAL_AREA_RADIUS = 10_000  # **10 km**
        self.DESTINATION_RADIUS = 2_000        # **2 km**
        self.MAX_DETOUR_MIN = 30               # **minutes**
        self.TIME_FLEXIBILITY_MIN = 30         # **minutes**
Adjust RESIDENTIAL_AREA_RADIUS or DESTINATION_RADIUS for matching areas.
Modify MAX_DETOUR_MIN or TIME_FLEXIBILITY_MIN for matching strictness.

🙋‍♂️ Contributing
We’d love your contributions! 🚀

Make changes locally in your project.
Test thoroughly to ensure compatibility.
Document new features in this README.


🎉 Acknowledgments
🗺️ Google Maps API for route calculations.
📍 Folium for interactive maps.
🖼️ PyQt5 for the GUI framework.
🔑 python-dotenv for secure configuration.
Built with ❤️ by fakhrialimin.
📬 Contact
Questions or ideas? Reach out:

GitHub: fakhrialimin

