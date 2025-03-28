from core.environment_manager import EnvironmentManager
import time

def test_environment_manager(cycles=5):
    # Create an instance of EnvironmentManager
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
        time.sleep(1)  # Wait 1 second (real-time) before next cycle


if __name__ == "__main__":
    test_environment_manager()
