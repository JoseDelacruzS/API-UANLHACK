#!/usr/bin/env python3
"""
🧪 Test script para verificar la integración Watson OpenAPI
"""

import requests
import json

# URLs de prueba
BASE_URL = "http://localhost:8001/api/v1"
OPENAPI_URL = f"{BASE_URL}/openapi/watson-openapi.json"
WATSON_ENDPOINTS = {
    "create_ticket": f"{BASE_URL}/watson/create-ticket",
    "schedule_visit": f"{BASE_URL}/watson/schedule-visit", 
    "get_status": f"{BASE_URL}/watson/get-status"
}

def test_openapi_spec():
    """Test OpenAPI specification"""
    print("🔍 Testing OpenAPI specification...")
    try:
        response = requests.get(OPENAPI_URL)
        if response.status_code == 200:
            spec = response.json()
            print(f"✅ OpenAPI spec loaded: {spec['info']['title']}")
            print(f"📋 Paths available: {list(spec['paths'].keys())}")
            return True
        else:
            print(f"❌ Error loading OpenAPI spec: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_create_ticket():
    """Test create ticket endpoint"""
    print("\n🎫 Testing create ticket endpoint...")
    try:
        payload = {
            "title": "Test ticket desde Python",
            "description": "Ticket de prueba para Watson",
            "priority": "medium",
            "client_ref": "CLI-TEST"
        }
        
        response = requests.post(
            WATSON_ENDPOINTS["create_ticket"],
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Ticket created: {result}")
            return True
        else:
            print(f"❌ Error creating ticket: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_schedule_visit():
    """Test schedule visit endpoint"""
    print("\n📅 Testing schedule visit endpoint...")
    try:
        payload = {
            "client_ref": "CLI-TEST",
            "visit_type": "mantenimiento",
            "preferred_date": "2024-12-15",
            "description": "Visita de prueba desde Python"
        }
        
        response = requests.post(
            WATSON_ENDPOINTS["schedule_visit"],
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Visit scheduled: {result}")
            return True
        else:
            print(f"❌ Error scheduling visit: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_status():
    """Test get status endpoint"""
    print("\n📊 Testing get status endpoint...")
    try:
        payload = {
            "query_type": "general"
        }
        
        response = requests.post(
            WATSON_ENDPOINTS["get_status"],
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status retrieved: {result}")
            return True
        else:
            print(f"❌ Error getting status: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 UANL Watson Integration Tests")
    print("=" * 50)
    
    # Test OpenAPI spec
    spec_ok = test_openapi_spec()
    
    if not spec_ok:
        print("\n❌ OpenAPI spec test failed. Make sure server is running on port 8001")
        return
    
    # Test endpoints
    create_ok = test_create_ticket()
    visit_ok = test_schedule_visit()
    status_ok = test_get_status()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"OpenAPI Spec: {'✅' if spec_ok else '❌'}")
    print(f"Create Ticket: {'✅' if create_ok else '❌'}")
    print(f"Schedule Visit: {'✅' if visit_ok else '❌'}")
    print(f"Get Status: {'✅' if status_ok else '❌'}")
    
    if all([spec_ok, create_ok, visit_ok, status_ok]):
        print("\n🎉 All tests passed! Watson integration ready!")
    else:
        print("\n⚠️  Some tests failed. Check server logs.")

if __name__ == "__main__":
    main()
