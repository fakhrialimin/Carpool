import folium
import io
from folium.plugins import AntPath
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QTextEdit, QPushButton,
    QComboBox, QSplitter, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QFont
from ui.widgets import RideListItem, LoadingWidget
from models.data_models import TripType
from services.matching import compute_matches

class CarpoolWindow(QMainWindow):
    def __init__(self, rides, ride_requests):
        super().__init__()
        self.rides = rides
        self.ride_requests = ride_requests
        self.current_ride = None
        self.current_request = None
        self.matrix = None
        self.init_ui()
        self.update_matrix()
        
    def init_ui(self):
        """
        Initialize the main window UI.
        """
        self.setWindowTitle("Tunisian Carpool Stuttgart")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_styles()
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)
        self.update_rides_list()

    def create_left_panel(self):
        """
        Create the left panel with controls.
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("Tunisische Fahrgemeinschaften Stuttgart")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(title)

        filter_panel = QWidget()
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.addWidget(QLabel("Filter:"))
        
        self.trip_filter = QComboBox()
        self.trip_filter.addItem("Alle Fahrten")
        self.trip_filter.addItem("Nur Hinfahrten")
        self.trip_filter.addItem("Nur Rückfahrten")
        self.trip_filter.currentIndexChanged.connect(self.apply_filters)
        
        self.seats_filter = QComboBox()
        self.seats_filter.addItem("Alle Sitzplätze")
        self.seats_filter.addItem("1+ verfügbar")
        self.seats_filter.addItem("2+ verfügbar")
        self.seats_filter.addItem("3+ verfügbar")
        self.seats_filter.currentIndexChanged.connect(self.apply_filters)
        
        filter_layout.addWidget(self.trip_filter)
        filter_layout.addWidget(self.seats_filter)
        layout.addWidget(filter_panel)

        self.rides_list = QListWidget()
        self.rides_list.setSelectionMode(QListWidget.SingleSelection)
        self.rides_list.itemSelectionChanged.connect(self.on_ride_selected)
        layout.addWidget(QLabel("Verfügbare Fahrten:"))
        layout.addWidget(self.rides_list)

        self.matches_list = QListWidget()
        self.matches_list.setSelectionMode(QListWidget.SingleSelection)
        self.matches_list.itemSelectionChanged.connect(self.on_match_selected)
        layout.addWidget(QLabel("Passende Mitfahrer:"))
        layout.addWidget(self.matches_list)

        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        
        self.add_rider_btn = QPushButton("Mitfahrer hinzufügen")
        self.add_rider_btn.clicked.connect(self.on_add_rider)
        self.add_rider_btn.setEnabled(False)
        
        self.remove_rider_btn = QPushButton("Mitfahrer entfernen")
        self.remove_rider_btn.clicked.connect(self.on_remove_rider)
        self.remove_rider_btn.setEnabled(False)
        
        button_layout.addWidget(self.add_rider_btn)
        button_layout.addWidget(self.remove_rider_btn)
        layout.addWidget(button_panel)

        return panel

    def create_right_panel(self):
        """
        Create the right panel with ride info and map.
        """
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        self.ride_info = QTextEdit()
        self.ride_info.setReadOnly(True)
        self.ride_info.setMinimumHeight(150)
        layout.addWidget(self.ride_info)

        self.map_view = QWebEngineView()
        self.map_view.setHtml(self.get_empty_map_html())
        layout.addWidget(self.map_view)

        return panel

    def setup_styles(self):
        """
        Apply styles to the UI components.
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QListWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QTextEdit {
                background: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    def update_matrix(self):
        """
        Calculate matching matrix between rides and requests.
        """
        self.matrix = compute_matches(self.rides, self.ride_requests)
        self.update_matches_list()

    def update_rides_list(self):
        """
        Update the list of available rides.
        """
        self.rides_list.clear()
        for ride in self.rides:
            seats_available = ride.available_seats - len(ride.matched_riders)
            trip_icon = "➡️" if ride.trip_type == TripType.OUTBOUND else "⬅️"
            
            item = RideListItem(f"""
                {trip_icon} {ride.driver.name}
                Von: {ride.start_point}
                Nach: {ride.end_point}
                Abfahrt: {ride.departure_time.strftime('%H:%M')}
                Plätze: {seats_available}/{ride.available_seats}
            """)
            item.setData(Qt.UserRole, ride)
            self.rides_list.addItem(item)

    def update_matches_list(self):
        """
        Update the list of matching ride requests.
        """
        self.matches_list.clear()
        if not self.current_ride:
            return
            
        if self.current_ride.driver.name in self.matrix:
            for match in self.matrix[self.current_ride.driver.name]:
                request = match['request']
                item = QListWidgetItem(f"""
                    {request.rider.name}
                    Von: {request.start_point}
                    Bewertung: {match['score']:.2f}
                    Umweg: {match['details']['detour_time']:.1f} min
                """)
                item.setData(Qt.UserRole, request)
                self.matches_list.addItem(item)

    def update_ride_info(self):
        """
        Update the ride information display.
        """
        if not self.current_ride:
            self.ride_info.setHtml("<p>Bitte wählen Sie eine Fahrt aus</p>")
            return
            
        ride = self.current_ride
        trip_type = "Hinfahrt zur Arbeit" if ride.trip_type == TripType.OUTBOUND else "Rückfahrt nach Hause"
        seats_available = ride.available_seats - len(ride.matched_riders)
        
        html = f"""
        <div style="font-family: Arial; color: #333;">
            <h3 style="color: #2c3e50;">{ride.driver.name} - {trip_type}</h3>
            <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
                <p><b>Von:</b> {ride.start_point}</p>
                <p><b>Nach:</b> {ride.end_point}</p>
                <p><b>Abfahrt:</b> {ride.departure_time.strftime('%H:%M')}</p>
                <p><b>Verfügbare Plätze:</b> 
                    <span style="color: {'#28a745' if seats_available > 0 else '#dc3545'}">
                        {seats_available}/{ride.available_seats}
                    </span>
                </p>
                <p><b>Maximaler Umweg:</b> {ride.max_detour_min} Minuten</p>
            </div>
        """
        
        if ride.matched_riders:
            html += "<h4 style='margin-top: 15px;'>Aktuelle Mitfahrer:</h4><ul>"
            for rider in ride.matched_riders:
                html += f"<li>{rider.rider.name} (von {rider.start_point})</li>"
            html += "</ul>"
        else:
            html += "<p style='color: #6c757d; margin-top: 10px;'>Keine Mitfahrer zugewiesen</p>"
            
        html += "</div>"
        self.ride_info.setHtml(html)

    def update_map(self):
        """
        Update the map display with the current ride's route.
        """
        if not self.current_ride:
            self.map_view.setHtml(self.get_empty_map_html())
            return
            
        loading = LoadingWidget("Karte wird geladen...")
        self.setCentralWidget(loading)
        
        try:
            avg_lat = (self.current_ride.start_coords.lat + self.current_ride.end_coords.lat) / 2
            avg_lng = (self.current_ride.start_coords.lng + self.current_ride.end_coords.lng) / 2
            m = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

            line_color = '#1f77b4' if self.current_ride.trip_type == TripType.OUTBOUND else '#ff7f0e'
            
            if self.current_ride.route_polyline:
                AntPath(
                    locations=self.current_ride.route_polyline,
                    color=line_color,
                    weight=5,
                    dash_array='5,5' if self.current_ride.trip_type == TripType.RETURN else None,
                    tooltip=f"{'Hinfahrt' if self.current_ride.trip_type == TripType.OUTBOUND else 'Rückfahrt'}"
                ).add_to(m)

            folium.Marker(
                location=(self.current_ride.start_coords.lat, self.current_ride.start_coords.lng),
                popup=f"Start: {self.current_ride.start_point}",
                icon=folium.Icon(color='green', icon='home')
            ).add_to(m)

            folium.Marker(
                location=(self.current_ride.end_coords.lat, self.current_ride.end_coords.lng),
                popup=f"Ziel: {self.current_ride.end_point}",
                icon=folium.Icon(color='red', icon='briefcase')
            ).add_to(m)

            for rider in self.current_ride.matched_riders:
                folium.Marker(
                    location=(rider.start_coords.lat, rider.start_coords.lng),
                    popup=f"Mitfahrer: {rider.rider.name}",
                    icon=folium.Icon(color='purple', icon='user')
                ).add_to(m)

            html_file = io.StringIO()
            m.save(html_file, close_file=False)
            self.map_view.setHtml(html_file.getvalue())
            html_file.close()
            
        except Exception as e:
            self.map_view.setHtml(f"""
                <h3>Karte konnte nicht geladen werden</h3>
                <p>Fehler: {str(e)}</p>
            """)
        finally:
            self.setCentralWidget(self.centralWidget())

    def get_empty_map_html(self):
        """
        Return HTML for an empty map view.
        """
        return """
        <html>
            <body style="background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100%;">
                <div style="text-align: center; color: #666;">
                    <h3>Keine Fahrt ausgewählt</h3>
                    <p>Bitte wählen Sie eine Fahrt aus der Liste</p>
                </div>
            </body>
        </html>
        """

    def apply_filters(self):
        """
        Apply filters to the rides list.
        """
        trip_filter = self.trip_filter.currentText()
        seats_filter = self.seats_filter.currentText()
        
        self.rides_list.clear()
        for ride in self.rides:
            seats_available = ride.available_seats - len(ride.matched_riders)
            show = True
            
            if trip_filter == "Nur Hinfahrten" and ride.trip_type != TripType.OUTBOUND:
                show = False
            elif trip_filter == "Nur Rückfahrten" and ride.trip_type != TripType.RETURN:
                show = False
                
            if seats_filter != "Alle Sitzplätze":
                min_seats = int(seats_filter[0])
                if seats_available < min_seats:
                    show = False
                    
            if show:
                item = RideListItem(f"""
                    {ride.driver.name}
                    Von: {ride.start_point}
                    Nach: {ride.end_point}
                    Abfahrt: {ride.departure_time.strftime('%H:%M')}
                    Plätze: {seats_available}/{ride.available_seats}
                """)
                item.setData(Qt.UserRole, ride)
                self.rides_list.addItem(item)

    def on_ride_selected(self):
        """
        Handle ride selection from the rides list.
        """
        selected = self.rides_list.selectedItems()
        if not selected:
            return
            
        self.current_ride = selected[0].data(Qt.UserRole)
        self.current_request = None
        self.update_ride_info()
        self.update_matches_list()
        self.update_map()
        self.update_button_states()

    def on_match_selected(self):
        """
        Handle match selection from the matches list.
        """
        selected = self.matches_list.selectedItems()
        if not selected:
            return
            
        self.current_request = selected[0].data(Qt.UserRole)
        self.update_map()
        self.update_button_states()

    def update_button_states(self):
        """
        Update the enabled state of action buttons.
        """
        has_selected_ride = self.current_ride is not None
        has_selected_request = self.current_request is not None
        
        can_add = (has_selected_ride and has_selected_request and
                   (self.current_ride.available_seats - len(self.current_ride.matched_riders)) > 0 and
                   self.current_request not in self.current_ride.matched_riders)
        
        can_remove = (has_selected_ride and has_selected_request and
                     self.current_request in self.current_ride.matched_riders)
        
        self.add_rider_btn.setEnabled(can_add)
        self.remove_rider_btn.setEnabled(can_remove)

    def on_add_rider(self):
        """
        Handle adding a rider to a ride.
        """
        if not (self.current_ride and self.current_request):
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie eine Fahrt und einen Mitfahrer aus")
            return
            
        if len(self.current_ride.matched_riders) >= self.current_ride.available_seats:
            QMessageBox.warning(self, "Fehler", "Keine freien Plätze mehr verfügbar")
            return
            
        self.current_request.accept_match(self.current_ride)
        self.update_matrix()
        self.update_ride_info()
        self.update_matches_list()
        self.update_map()
        QMessageBox.information(self, "Erfolg", f"{self.current_request.rider.name} wurde hinzugefügt")

    def on_remove_rider(self):
        """
        Handle removing a rider from a ride.
        """
        if not (self.current_ride and self.current_request):
            QMessageBox.warning(self, "Fehler", "Bitte wählen Sie eine Fahrt und einen Mitfahrer aus")
            return
            
        if self.current_request not in self.current_ride.matched_riders:
            QMessageBox.warning(self, "Fehler", "Dieser Mitfahrer ist nicht in der ausgewählten Fahrt")
            return
            
        self.current_ride.remove_rider(self.current_request)
        self.current_request.matched_ride = None
        self.update_matrix()
        self.update_ride_info()
        self.update_matches_list()
        self.update_map()
        QMessageBox.information(self, "Erfolg", f"{self.current_request.rider.name} wurde entfernt")