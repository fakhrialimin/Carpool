import unittest
from utils.helpers import haversine_distance, Coordinates

class TestHelpers(unittest.TestCase):
    def test_haversine_distance(self):
        """
        Test haversine distance calculation.
        """
        coord1 = Coordinates(lat=48.7758, lng=9.1829)
        coord2 = Coordinates(lat=48.7833, lng=9.2250)
        distance = haversine_distance(coord1, coord2)
        self.assertAlmostEqual(distance, 2950, delta=100)  # Approx 2.95km

if __name__ == '__main__':
    unittest.main()