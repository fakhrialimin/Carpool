# 🚗 Carpool

**Carpool** is a Python-based ride-sharing application that connects _drivers_ and _passengers_ heading in the same direction.  
It uses the **Google Maps Directions API** to calculate optimal routes, estimate travel time, and minimize detours — promoting efficient and eco-friendly commuting.

---

## ✨ Features

- **Route Calculation**: Powered by Google Maps to calculate distance, duration, and route paths.
- **Smart Matching**: Configurable detour and time flexibility settings for intelligent driver-passenger pairing.
- **Modular Design**: Organized into configuration, data models, services, UI, and utility modules.
- **Secure Config**: Uses `.env` for API key management to keep credentials out of source control.

---

## 📁 Project Structure

Carpool/
├── config/ # Configuration settings
├── models/ # Data models (e.g., Coordinates)
├── services/ # Routing logic and API calls
├── ui/ # User interface logic
├── utils/ # Helper functions
├── main.py # Application entry point
├── requirements.txt # Python dependencies
├── .gitignore # Ignored files
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- A Google Maps API key

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/fakhrialimin/Carpool.git
   cd Carpool
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file
In the root directory, add your Google Maps API key:

ini
Copy
Edit
GMAPS_API_KEY=your_api_key_here
Run the application

bash
Copy
Edit
python main.py
🧪 Running Tests
To run all tests in the tests/ folder:

bash
Copy
Edit
python -m unittest discover tests
⚙️ Configuration
You can adjust the following in config/settings.py:

python
Copy
Edit
GMAPS_API_KEY = "your_key_here"
RESIDENTIAL_AREA_RADIUS = 10000       # in meters
DESTINATION_RADIUS = 2000             # in meters
MAX_DETOUR_MIN = 30                   # in minutes
TIME_FLEXIBILITY_MIN = 30             # in minutes
📄 License
This project is licensed under the Uni 'Stuttgart license

🙋‍♂️ Contributing
Contributions are welcome! Feel free to fork the repo and submit pull requests.

🧠 Author
Built with ❤️ by fakhrialimin
