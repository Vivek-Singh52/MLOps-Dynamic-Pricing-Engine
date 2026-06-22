import time
import random
import requests

API_URL = "http://localhost:8000/predict"

def simulate_traffic():
    print(f"Starting traffic simulation against {API_URL}...")
    while True:
        # Simulate drift by changing the distribution over time or adding occasional spikes
        is_drift = random.random() < 0.1 # 10% chance of drift/spike
        
        payload = {
            "time_of_day": random.randint(0, 23),
            "weather_condition": random.randint(0, 2),
            "demand_multiplier": random.uniform(2.5, 3.0) if is_drift else random.uniform(0.5, 1.5),
            "base_price": random.uniform(10.0, 15.0)
        }
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                print(f"Success: {payload} -> {response.json()['optimal_price']}")
            else:
                print(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    simulate_traffic()
