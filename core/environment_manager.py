import datetime
import random
import yaml


class EnvironmentManager:
    """
    Manages the simulation environment including accelerated time, seasonal weather,
    and day/night cycles for the Smart Apartment IoT system.
    """

    def __init__(self, config_path='../config.yaml'):
        """Initializes the environment manager with settings loaded from config file."""
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.acceleration_factor = self.config['simulation']['time_acceleration_factor']
        self.simulated_time = datetime.datetime.now()
        self.current_season = self.get_current_season()

    def get_current_season(self):
        """Determines the current season based on the simulated month."""
        month = self.simulated_time.month
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'

    def update_time(self):
        """Advances the simulated time based on the acceleration factor."""
        real_seconds_passed = 1
        simulated_minutes_passed = real_seconds_passed * self.acceleration_factor
        self.simulated_time += datetime.timedelta(minutes=simulated_minutes_passed)
        self.current_season = self.get_current_season()

    def is_daytime(self):
        """Determines whether it is currently day or night in the simulation."""
        sunrise, sunset = self.get_sun_times()
        current_time = self.simulated_time.time()
        return sunrise <= current_time <= sunset

    def get_sun_times(self):
        """Returns sunrise and sunset times based on the current season."""
        sun_times = {
            'Winter': (datetime.time(7, 0), datetime.time(17, 0)),
            'Spring': (datetime.time(6, 0), datetime.time(18, 30)),
            'Summer': (datetime.time(5, 30), datetime.time(19, 30)),
            'Autumn': (datetime.time(6, 30), datetime.time(18, 0)),
        }
        return sun_times[self.current_season]

    def current_temperature(self):
        """Generates current temperature based on the current season."""
        seasonal_temperatures = {
            'Winter': (5, 15),
            'Spring': (15, 25),
            'Summer': (25, 35),
            'Autumn': (15, 25)
        }
        min_temp, max_temp = seasonal_temperatures[self.current_season]
        return round(random.uniform(min_temp, max_temp), 1)

    def current_weather_condition(self):
        """Determines weather condition based on season and current temperature."""
        conditions = None
        temp = self.current_temperature()
        season = self.current_season

        if season == 'Winter':
            if temp <= 7:
                conditions = ['Snowy', 'Rainy', 'Cloudy']
            elif temp <= 12:
                conditions = ['Rainy', 'Cloudy']
            else:
                conditions = ['Clear', 'Cloudy']

        elif season == 'Spring':
            if temp <= 18:
                conditions = ['Rainy', 'Cloudy']
            else:
                conditions = ['Clear', 'Cloudy']

        elif season == 'Summer':
            if temp >= 30:
                conditions = ['Hot', 'Clear', 'Sunny']
            else:
                conditions = ['Clear', 'Sunny', 'Cloudy']

        elif season == 'Autumn':
            if temp <= 18:
                conditions = ['Rainy', 'Windy', 'Cloudy']
            else:
                conditions = ['Clear', 'Cloudy', 'Windy']

        return random.choice(conditions)

    def get_environment_data(self):
        """Provides current environmental data to other system components."""
        return {
            'timestamp': self.simulated_time.isoformat(),
            'season': self.current_season,
            'is_daytime': self.is_daytime(),
            'temperature': self.current_temperature(),
            'weather_condition': self.current_weather_condition()
        }


# Example of usage
if __name__ == '__main__':
    env_manager = EnvironmentManager()
    for _ in range(10):
        env_manager.update_time()
        data = env_manager.get_environment_data()
        print(data)