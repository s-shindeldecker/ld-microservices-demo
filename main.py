import os
import random
import requests
import time
from dotenv import load_dotenv
import ldclient
from ldclient.config import Config
import json

load_dotenv()

# Initialize the LaunchDarkly client
ld_sdk_key = os.getenv('LD_SDK_KEY')
if not ld_sdk_key:
    raise Exception("Please set LD_SDK_KEY in .env file")

ldclient.set_config(Config(ld_sdk_key))
ld_client = ldclient.get()

# Service endpoints
SERVICE_A_URL = "http://localhost:8001/sort"
SERVICE_B_URL = "http://localhost:8002/sort"

def get_random_numbers(size=1000):
    """Generate a list of random numbers"""
    return [random.randint(1, 10000) for _ in range(size)]

def process_with_service(service_url, numbers):
    """Send numbers to specified service for processing"""
    try:
        response = requests.post(
            service_url,
            json={"numbers": numbers},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print(f"Error calling service: {str(e)}")
        return None

def run_experiment():
    """Run the experiment using LaunchDarkly for traffic routing"""
    numbers = get_random_numbers()
    
    # Create a user context for LaunchDarkly
    context = {
        "key": f"user-{int(time.time())}",
        "kind": "user"
    }
    
    # Get the variation from LaunchDarkly
    should_use_optimized = ld_client.variation(
        "use-optimized-service",
        context,
        False
    )
    
    # Route to appropriate service based on the feature flag
    service_url = SERVICE_B_URL if should_use_optimized else SERVICE_A_URL
    result = process_with_service(service_url, numbers)
    
    if result:
        # Send metrics back to LaunchDarkly
        metric_value = result.get("processing_time", 0)
        ld_client.track(
            "sorting-performance",
            context,
            metric_value=metric_value
        )
        
        print(f"\nExperiment Results:")
        print(f"Service Used: {result['service']}")
        print(f"Processing Time: {result['processing_time']:.6f} seconds")
        print(f"First few sorted numbers: {result['sorted_array'][:5]}...")

def main():
    print("LaunchDarkly Microservices Experiment Demo")
    print("=========================================")
    
    try:
        while True:
            input("\nPress Enter to run an experiment (Ctrl+C to exit)...")
            run_experiment()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        ld_client.close()

if __name__ == "__main__":
    main()
