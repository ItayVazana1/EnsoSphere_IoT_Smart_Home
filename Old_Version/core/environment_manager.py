import datetime
import random
import yaml
import logging
import os

class EnvironmentManager:
    """
    Manages the simulation environment including accelerated time, seasonal weather,
    and day/night cycles for the Smart Apartment IoT system.
    """

    import os

    def __init__(self, config_path=None):
        """Initializes the environment manager with settings loaded from config file."""
        if config_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            config_path = os.path.join(base_dir, 'config.yaml')

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

        self.acceleration_factor = self.config['simulation']['time_acceleration_factor']

        # Randomize initial simulation date within the specified year
        simulation_year = self.config['simulation'].get('simulation_year', datetime.datetime.now().year)
        random_month = random.randint(1, 12)
        random_day = random.randint(1, 28)
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)

        self.simulated_time = datetime.datetime(
            simulation_year, random_month, random_day, random_hour, random_minute
        )

        self.current_season = self.get_current_season()
        self.current_temp = self.current_temperature()
        self.current_weather = self.current_weather_condition()
        self.last_weather_update_hour = self.simulated_time.hour

        logging.info(f"Simulation start date randomly set to: {self.simulated_time.isoformat()}")

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
        self.update_weather_hourly()

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
        temp = self.current_temp
        season = self.current_season

        if season == 'Winter':
            conditions = ['Snowy', 'Rainy', 'Cloudy'] if temp <= 7 else ['Rainy', 'Cloudy'] if temp <= 12 else ['Clear', 'Cloudy']
        elif season == 'Spring':
            conditions = ['Rainy', 'Cloudy'] if temp <= 18 else ['Clear', 'Cloudy']
        elif season == 'Summer':
            conditions = ['Hot', 'Clear', 'Sunny'] if temp >= 30 else ['Clear', 'Sunny', 'Cloudy']
        elif season == 'Autumn':
            conditions = ['Rainy', 'Windy', 'Cloudy'] if temp <= 18 else ['Clear', 'Cloudy', 'Windy']

        return random.choice(conditions)

    def update_weather_hourly(self):
        """Updates weather conditions once per simulated hour."""
        current_hour = self.simulated_time.hour
        if current_hour != self.last_weather_update_hour:
            self.current_temp = self.current_temperature()
            self.current_weather = self.current_weather_condition()
            self.last_weather_update_hour = current_hour

            logging.info(
                f"Weather updated: Temp={self.current_temp}, Condition={self.current_weather}, Hour={current_hour}"
            )

    def get_environment_data(self):
        """Provides current environmental data to other system components."""
        return {
            'timestamp': self.simulated_time.isoformat(),
            'season': self.current_season,
            'is_daytime': self.is_daytime(),
            'temperature': self.current_temp,
            'weather_condition': self.current_weather
        }


# Example of usage
if __name__ == '__main__':
    env_manager = EnvironmentManager()
    for _ in range(10):
        env_manager.update_time()
        data = env_manager.get_environment_data()
        print(data)