import os
import random
import requests
import time
import uuid
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
    
    # Create a user context for LaunchDarkly with UUID
    context = {
        "key": str(uuid.uuid4()),
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
        print(f"User Key: {context['key']}")
        print(f"Service Used: {result['service']}")
        print(f"Processing Time: {result['processing_time']:.6f} seconds")
        print(f"First few sorted numbers: {result['sorted_array'][:5]}...")
        return result
    return None

def run_batch(num_records):
    """Run a batch of experiments"""
    print(f"\nRunning batch of {num_records} experiments...")
    
    successful_runs = 0
    total_time = 0
    service_a_count = 0
    service_b_count = 0
    
    for i in range(num_records):
        print(f"\nProcessing record {i + 1}/{num_records}")
        result = run_experiment()
        
        if result:
            successful_runs += 1
            total_time += result['processing_time']
            if result['service'] == 'Service A':
                service_a_count += 1
            else:
                service_b_count += 1
    
    # Print batch summary
    print("\nBatch Processing Summary")
    print("=======================")
    print(f"Total Records Processed: {num_records}")
    print(f"Successful Runs: {successful_runs}")
    print(f"Failed Runs: {num_records - successful_runs}")
    if successful_runs > 0:
        print(f"Average Processing Time: {total_time/successful_runs:.6f} seconds")
        print(f"Service A Usage: {service_a_count} ({service_a_count/num_records*100:.1f}%)")
        print(f"Service B Usage: {service_b_count} ({service_b_count/num_records*100:.1f}%)")

def main():
    print("LaunchDarkly Microservices Experiment Demo")
    print("=========================================")
    
    try:
        while True:
            print("\nSelect mode:")
            print("1. Interactive Mode (Press Enter for each experiment)")
            print("2. Batch Mode (Process multiple records)")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                while True:
                    try:
                        input("\nPress Enter to run an experiment (Ctrl+C to return to menu)...")
                        run_experiment()
                    except KeyboardInterrupt:
                        print("\nReturning to menu...")
                        break
            elif choice == "2":
                while True:
                    try:
                        num_records = input("\nEnter number of records to process (or 'back' to return to menu): ").strip()
                        if num_records.lower() == 'back':
                            break
                        num_records = int(num_records)
                        if num_records <= 0:
                            print("Please enter a positive number")
                            continue
                        run_batch(num_records)
                        break
                    except ValueError:
                        print("Please enter a valid number")
                    except KeyboardInterrupt:
                        print("\nReturning to menu...")
                        break
            elif choice == "3":
                print("\nShutting down...")
                break
            else:
                print("\nInvalid choice. Please select 1, 2, or 3.")
    finally:
        ld_client.close()

if __name__ == "__main__":
    main()
