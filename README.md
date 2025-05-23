# Carpool
🚗 Carpool
Carpool is a Python-based application designed to facilitate ride-sharing by connecting drivers and passengers heading in the same direction. It leverages the Google Maps Directions API to calculate optimal routes, estimate travel times, and minimize detours, promoting efficient and eco-friendly commuting.

🧩 Features
Route Calculation: Utilizes the Google Maps Directions API to compute distances, durations, and polylines between origins and destinations.

Flexible Matching: Incorporates configurable parameters such as maximum detour time and time flexibility to match drivers and passengers effectively.

Modular Architecture: Structured with clear separation of concerns, including configuration, data models, services, UI, and utilities.

Environment Configuration: Manages sensitive information like API keys through environment variables for enhanced security.

🗂️ Project Structure
bash
Copy
Edit
Carpool/
├── config/           # Configuration settings and environment variables
├── models/           # Data models (e.g., Coordinates)
├── services/         # Core services (e.g., routing logic)
├── ui/               # User interface components
├── utils/            # Utility functions
├── tests/            # Unit tests
├── main.py           # Entry point of the application
├── requirements.txt  # Python dependencies
├── .gitignore        # Specifies files to ignore in version control
└── README.md         # Project documentation
🚀 Getting Started
Prerequisites
Python 3.8 or higher

A Google Maps API key

Installation
Clone the Repository

bash
Copy
Edit
git clone https://github.com/fakhrialimin/Carpool.git
cd Carpool
Create a Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set Up Environment Variables

Create a .env file in the root directory and add your Google Maps API key:

ini
Copy
Edit
GMAPS_API_KEY=your_api_key_here
Run the Application

bash
Copy
Edit
python main.py
🧪 Running Tests
To execute the unit tests:

bash
Copy
Edit
python -m unittest discover tests
🛠️ Configuration
Adjust the following parameters in config/settings.py to fine-tune the application's behavior:

RESIDENTIAL_AREA_RADIUS: Radius (in meters) to consider for residential areas.

DESTINATION_RADIUS: Radius (in meters) around the destination for matching.

MAX_DETOUR_MIN: Maximum allowable detour time in minutes.

TIME_FLEXIBILITY_MIN: Time flexibility in minutes for matching rides.
