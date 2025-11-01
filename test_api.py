"""
API Test Script
Save as: ~/chakravyuh/brahmastra/test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_playbooks():
    """Test playbooks listing"""
    print("🔍 Testing /playbooks...")
    response = requests.get(f"{BASE_URL}/playbooks")
    print(f"Status: {response.status_code}")
    playbooks = response.json()
    print(f"Found {len(playbooks)} playbooks")
    for pb in playbooks:
        print(f"  - {pb['name']} ({pb['severity']})")
    print()

def test_threat_response():
    """Test threat handling"""
    print("🔍 Testing /threats...")
    
    threat_data = {
        "source_ip": "203.0.113.45",
        "target_ip": "10.0.0.10",
        "target_ports": [22],
        "severity": "HIGH",
        "threat_type": "intrusion",
        "description": "API test - SSH brute force",
        "confidence_score": 0.95
    }
    
    response = requests.post(f"{BASE_URL}/threats", json=threat_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2))
    print()

def test_stats():
    """Test statistics"""
    print("🔍 Testing /stats...")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("BRAHMASTRA API TESTING")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_playbooks()
        test_threat_response()
        test_stats()
        
        print("✅ All tests completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
