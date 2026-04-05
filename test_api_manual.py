#!/usr/bin/env python3
"""
Manual API testing script for ShipIQ Cargo Optimization Service.
Run this after starting the server to verify all endpoints work correctly.
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000/api/v1"


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_response(response: requests.Response):
    """Print formatted response."""
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Success")
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print("❌ Failed")
        print(response.text)


def test_health_check():
    """Test health check endpoint."""
    print_section("Test 1: Health Check")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    return response.status_code == 200


def test_simple_optimization():
    """Test simple optimization."""
    print_section("Test 2: Simple Optimization")
    
    payload = {
        "cargos": [
            {"id": "C1", "volume": 1234},
            {"id": "C2", "volume": 4352}
        ],
        "tanks": [
            {"id": "T1", "capacity": 5000},
            {"id": "T2", "capacity": 3000}
        ]
    }
    
    print("Request:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/optimize", json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Metrics Summary:")
        print(f"  Total Cargo Volume: {data['metrics']['total_cargo_volume']}")
        print(f"  Total Tank Capacity: {data['metrics']['total_tank_capacity']}")
        print(f"  Total Loaded: {data['metrics']['total_loaded_volume']}")
        print(f"  Tank Utilization: {data['metrics']['tank_utilization_percentage']}%")
        print(f"  Cargo Loaded: {data['metrics']['cargo_loaded_percentage']}%")
        print(f"  Number of Allocations: {data['metrics']['number_of_allocations']}")
    
    return response.status_code == 200


def test_sample_data():
    """Test with assignment sample data."""
    print_section("Test 3: Sample Data from Assignment")
    
    response = requests.post(f"{BASE_URL}/optimize/sample")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Metrics Summary:")
        print(f"  Total Cargo Volume: {data['metrics']['total_cargo_volume']}")
        print(f"  Total Tank Capacity: {data['metrics']['total_tank_capacity']}")
        print(f"  Total Loaded: {data['metrics']['total_loaded_volume']}")
        print(f"  Tank Utilization: {data['metrics']['tank_utilization_percentage']}%")
        print(f"  Cargo Loaded: {data['metrics']['cargo_loaded_percentage']}%")
        print(f"  Tanks Used: {data['metrics']['tanks_used']}/{data['metrics']['tanks_total']}")
        
        if data['unallocated_cargo']:
            print(f"\n⚠️  Unallocated Cargo:")
            for cargo in data['unallocated_cargo']:
                print(f"    {cargo['cargo_id']}: {cargo['unallocated_volume']} units")
    
    return response.status_code == 200


def test_cargo_splitting():
    """Test cargo splitting across multiple tanks."""
    print_section("Test 4: Cargo Splitting")
    
    payload = {
        "cargos": [
            {"id": "C1", "volume": 500}
        ],
        "tanks": [
            {"id": "T1", "capacity": 200},
            {"id": "T2", "capacity": 200},
            {"id": "T3", "capacity": 200}
        ]
    }
    
    print("Request:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/optimize", json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Cargo C1 split across {len(data['allocations'])} tanks")
        for alloc in data['allocations']:
            print(f"  {alloc['tank_id']}: {alloc['volume_allocated']} units")
    
    return response.status_code == 200


def test_validation_errors():
    """Test input validation."""
    print_section("Test 5: Input Validation")
    
    test_cases = [
        {
            "name": "Negative volume",
            "payload": {
                "cargos": [{"id": "C1", "volume": -100}],
                "tanks": [{"id": "T1", "capacity": 1000}]
            }
        },
        {
            "name": "Duplicate cargo IDs",
            "payload": {
                "cargos": [
                    {"id": "C1", "volume": 100},
                    {"id": "C1", "volume": 200}
                ],
                "tanks": [{"id": "T1", "capacity": 1000}]
            }
        },
        {
            "name": "Empty cargo list",
            "payload": {
                "cargos": [],
                "tanks": [{"id": "T1", "capacity": 1000}]
            }
        }
    ]
    
    all_passed = True
    for test_case in test_cases:
        print(f"\n  Testing: {test_case['name']}")
        response = requests.post(f"{BASE_URL}/optimize", json=test_case['payload'])
        if response.status_code == 422:
            print(f"  ✅ Correctly rejected (422)")
        else:
            print(f"  ❌ Expected 422, got {response.status_code}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("\n" + "🚢" * 30)
    print("  ShipIQ Cargo Optimization Service - API Tests")
    print("🚢" * 30)
    
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the server is running (python -m app.main)")
    
    try:
        results = {
            "Health Check": test_health_check(),
            "Simple Optimization": test_simple_optimization(),
            "Sample Data": test_sample_data(),
            "Cargo Splitting": test_cargo_splitting(),
            "Input Validation": test_validation_errors()
        }
        
        print_section("Test Results Summary")
        for test_name, passed in results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        if all_passed:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️  Some tests failed. Check the output above.")
        
        return 0 if all_passed else 1
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the server is running:")
        print("  python -m app.main")
        print("  or")
        print("  ./run.sh")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
