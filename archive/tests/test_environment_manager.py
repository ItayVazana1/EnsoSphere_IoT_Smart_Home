import time
import datetime
import unittest
from core.environment_manager import EnvironmentManager


class TestEnvironmentManager(unittest.TestCase):
    """Unit tests for the EnvironmentManager class."""

    def setUp(self):
        """Set up the environment manager instance for testing."""
        self.env_manager = EnvironmentManager()

    def test_initialization(self):
        """Test initial state after creating an instance."""
        data = self.env_manager.get_environment_data()
        self.assertIn(data['season'], ['Winter', 'Spring', 'Summer', 'Autumn'])
        self.assertIsInstance(data['is_daytime'], bool)
        self.assertIsInstance(data['temperature'], float)
        self.assertIsInstance(data['weather_condition'], str)

    def test_environment_data_structure(self):
        """Verify structure of full environment data dictionary."""
        data = self.env_manager.get_environment_data()
        expected_keys = ['timestamp', 'season', 'is_daytime', 'temperature', 'weather_condition']
        for key in expected_keys:
            self.assertIn(key, data)

    def test_time_advancement(self):
        """Test simulated time advancement."""
        initial_time = self.env_manager.simulated_time
        self.env_manager.update_time()
        advanced_time = self.env_manager.simulated_time
        self.assertGreater(advanced_time, initial_time)

    def test_season_transition(self):
        """Forcefully test seasonal transitions."""
        test_dates = {
            datetime.datetime(2025, 1, 15): 'Winter',
            datetime.datetime(2025, 4, 15): 'Spring',
            datetime.datetime(2025, 7, 15): 'Summer',
            datetime.datetime(2025, 10, 15): 'Autumn',
        }
        for date, expected_season in test_dates.items():
            self.env_manager.simulated_time = date
            self.assertEqual(self.env_manager.get_current_season(), expected_season)

    def test_day_night_cycle(self):
        """Test correctness of day/night determination."""
        self.env_manager.simulated_time = datetime.datetime(2025, 6, 21, 12, 0)
        self.assertTrue(self.env_manager.is_daytime())

        self.env_manager.simulated_time = datetime.datetime(2025, 6, 21, 23, 0)
        self.assertFalse(self.env_manager.is_daytime())

    def test_temperature_ranges(self):
        """Ensure temperatures generated are within expected ranges."""
        season_ranges = {
            'Winter': (5, 15),
            'Spring': (15, 25),
            'Summer': (25, 35),
            'Autumn': (15, 25)
        }
        for season, (min_temp, max_temp) in season_ranges.items():
            self.env_manager.current_season = season
            for _ in range(10):
                temp = self.env_manager.current_temperature()
                self.assertGreaterEqual(temp, min_temp)
                self.assertLessEqual(temp, max_temp)

    def test_weather_conditions_validity(self):
        """Verify weather conditions are valid for each season and temperature."""
        conditions_per_season = {
            'Winter': ['Snowy', 'Rainy', 'Cloudy', 'Clear'],
            'Spring': ['Rainy', 'Cloudy', 'Clear'],
            'Summer': ['Hot', 'Clear', 'Sunny', 'Cloudy'],
            'Autumn': ['Rainy', 'Windy', 'Cloudy', 'Clear']
        }
        for season in conditions_per_season:
            self.env_manager.current_season = season
            for _ in range(10):
                self.env_manager.current_temp = self.env_manager.current_temperature()
                condition = self.env_manager.current_weather_condition()
                self.assertIn(condition, conditions_per_season[season])


# Optional interactive simulation
def run_interactive_test(cycles=5):
    env_manager = EnvironmentManager()
    for cycle in range(cycles):
        env_manager.update_time()
        data = env_manager.get_environment_data()
        print(f"Cycle {cycle + 1}:")
        print(f"  Simulated Time: {data['timestamp']}")
        print(f"  Season: {data['season']}")
        print(f"  Daytime: {'Yes' if data['is_daytime'] else 'No'}")
        print(f"  Temperature: {data['temperature']}°C")
        print(f"  Weather Condition: {data['weather_condition']}")
        print("-" * 40)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
    # run_interactive_test()  # Optional: uncomment to observe live behavior
