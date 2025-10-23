#!/usr/bin/env python3
"""
Test script to generate sample traffic and populate Grafana metrics
"""

import requests
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

API_BASE_URL = "http://localhost:6060"

# Test data variations
GOALS = ['Weight Loss', 'Muscle Gain', 'Weight Maintenance', 'Athletic Performance']
DIET_PREFS = ['Vegetarian', 'Non-Vegetarian', 'Vegan', 'Pescatarian', 'Keto', 'No Preference']
ACTIVITY_LEVELS = ['Sedentary', 'Lightly Active', 'Moderately Active', 'Very Active', 'Extremely Active']
GENDERS = ['M', 'F', 'Other']

def generate_random_user_data():
    """Generate random user data for testing"""
    return {
        'goal': random.choice(GOALS),
        'diet_preference': random.choice(DIET_PREFS),
        'age': random.randint(18, 65),
        'gender': random.choice(GENDERS),
        'weight': random.randint(50, 120),
        'height': random.randint(150, 200),
        'activity_level': random.choice(ACTIVITY_LEVELS),
        'allergies': random.choice(['None', 'Peanuts', 'Dairy', 'Gluten']),
        'dislikes': random.choice(['None', 'Mushrooms', 'Fish', 'Beans']),
        'meals_per_day': random.choice([3, 4, 5])
    }

def test_health_check():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        print(f"✓ Health Check: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False

def test_options():
    """Test options endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/options")
        print(f"✓ Options: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Options Failed: {e}")
        return False

def test_diet_plan(user_data):
    """Generate a diet plan"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/diet-plan",
            json=user_data,
            timeout=60
        )
        
        status = "✓" if response.status_code == 200 else "✗"
        print(f"{status} Diet Plan [{user_data['goal']}]: {response.status_code}")
        
        return response.status_code == 200
    except requests.Timeout:
        print(f"✗ Diet Plan Timeout: {user_data['goal']}")
        return False
    except Exception as e:
        print(f"✗ Diet Plan Error: {e}")
        return False

def test_quick_diet_plan():
    """Test quick diet plan endpoint"""
    try:
        data = {
            'goal': random.choice(GOALS),
            'diet_preference': random.choice(DIET_PREFS)
        }
        response = requests.post(
            f"{API_BASE_URL}/api/diet-plan/quick",
            json=data,
            timeout=60
        )
        print(f"✓ Quick Plan: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Quick Plan Failed: {e}")
        return False

def test_invalid_request():
    """Test error handling with invalid data"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/diet-plan",
            json={'invalid': 'data'},
            timeout=10
        )
        print(f"✓ Invalid Request (Expected 400): {response.status_code}")
        return response.status_code == 400
    except Exception as e:
        print(f"✗ Invalid Request Test Failed: {e}")
        return False

def test_404():
    """Test 404 handling"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/nonexistent")
        print(f"✓ 404 Test: {response.status_code}")
        return response.status_code == 404
    except Exception as e:
        print(f"✗ 404 Test Failed: {e}")
        return False

def run_load_test(num_requests=10, workers=3):
    """Run concurrent load test"""
    print(f"\n{'='*60}")
    print(f"Running Load Test: {num_requests} requests with {workers} workers")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    success_count = 0
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for i in range(num_requests):
            user_data = generate_random_user_data()
            future = executor.submit(test_diet_plan, user_data)
            futures.append(future)
            time.sleep(0.5)  # Stagger requests
        
        for future in futures:
            if future.result():
                success_count += 1
    
    duration = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"Load Test Results:")
    print(f"  Total Requests: {num_requests}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {num_requests - success_count}")
    print(f"  Duration: {duration:.2f}s")
    print(f"  Avg Time/Request: {duration/num_requests:.2f}s")
    print(f"{'='*60}\n")

def continuous_test(duration_minutes=5, delay_seconds=10):
    """Run continuous test for specified duration"""
    print(f"\n{'='*60}")
    print(f"Running Continuous Test for {duration_minutes} minutes")
    print(f"Request every {delay_seconds} seconds")
    print(f"{'='*60}\n")
    
    end_time = time.time() + (duration_minutes * 60)
    request_count = 0
    
    while time.time() < end_time:
        request_count += 1
        print(f"\n--- Request {request_count} at {datetime.now().strftime('%H:%M:%S')} ---")
        
        # Mix of different request types
        test_type = random.choice(['diet_plan', 'quick', 'health', 'options'])
        
        if test_type == 'diet_plan':
            user_data = generate_random_user_data()
            test_diet_plan(user_data)
        elif test_type == 'quick':
            test_quick_diet_plan()
        elif test_type == 'health':
            test_health_check()
        else:
            test_options()
        
        time.sleep(delay_seconds)
    
    print(f"\n{'='*60}")
    print(f"Continuous Test Complete: {request_count} total requests")
    print(f"{'='*60}\n")

def main():
    """Main test runner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         Diet Plan API - Metrics Test Generator               ║
    ║              Populate Grafana Dashboards                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("Testing API endpoints...")
    print(f"{'='*60}\n")
    
    # Basic tests
    if not test_health_check():
        print("\n✗ API is not responding. Make sure it's running on port 6060")
        return
    
    test_options()
    test_404()
    test_invalid_request()
    
    print("\n" + "="*60)
    print("Select Test Mode:")
    print("="*60)
    print("1. Quick Test (5 requests)")
    print("2. Load Test (20 requests, 3 workers)")
    print("3. Heavy Load (50 requests, 5 workers)")
    print("4. Continuous (5 minutes, request every 10s)")
    print("5. Continuous (15 minutes, request every 5s)")
    print("6. Custom Test")
    print("="*60)
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '1':
        run_load_test(num_requests=5, workers=2)
    elif choice == '2':
        run_load_test(num_requests=20, workers=3)
    elif choice == '3':
        run_load_test(num_requests=50, workers=5)
    elif choice == '4':
        continuous_test(duration_minutes=5, delay_seconds=10)
    elif choice == '5':
        continuous_test(duration_minutes=15, delay_seconds=5)
    elif choice == '6':
        num = int(input("Number of requests: "))
        workers = int(input("Number of concurrent workers: "))
        run_load_test(num_requests=num, workers=workers)
    else:
        print("Invalid choice. Running quick test...")
        run_load_test(num_requests=5, workers=2)
    
    print("\n✓ Test complete! Check your Grafana dashboard at http://localhost:3000")
    print("\nMetrics endpoint: http://localhost:6060/metrics")
    print("Prometheus: http://localhost:9090")

if __name__ == '__main__':
    main()