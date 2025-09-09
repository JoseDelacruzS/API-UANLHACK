#!/usr/bin/env python3
"""
Script de prueba para la API UANL Hack
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000/api/v1"
headers = {"Content-Type": "application/json"}

def test_health_check():
    """Probar endpoint de salud"""
    print("🔍 Probando health check...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check OK:", response.json())
        else:
            print("❌ Health check falló:", response.status_code)
    except Exception as e:
        print("❌ Error en health check:", str(e))

def test_root_endpoint():
    """Probar endpoint raíz"""
    print("\n🔍 Probando endpoint raíz...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Endpoint raíz OK:", response.json())
        else:
            print("❌ Endpoint raíz falló:", response.status_code)
    except Exception as e:
        print("❌ Error en endpoint raíz:", str(e))

def test_operators_endpoint():
    """Probar endpoint de operadores"""
    print("\n🔍 Probando endpoint de operadores...")
    try:
        # Obtener lista de operadores
        response = requests.get(f"{BASE_URL}/operators/", headers=headers)
        if response.status_code == 200:
            print("✅ GET operadores OK:", response.json())
        else:
            print("❌ GET operadores falló:", response.status_code, response.text)
            
        # Crear nuevo operador
        operator_data = {
            "name": f"Operador Test {datetime.now().strftime('%H%M%S')}"
        }
        response = requests.post(f"{BASE_URL}/operators/", 
                               headers=headers, 
                               json=operator_data)
        if response.status_code == 201:
            print("✅ POST operador OK:", response.json())
            return response.json()["operator_id"]
        else:
            print("❌ POST operador falló:", response.status_code, response.text)
            
    except Exception as e:
        print("❌ Error en endpoint de operadores:", str(e))
    
    return None

def test_dashboard_endpoint():
    """Probar endpoint de dashboard"""
    print("\n🔍 Probando endpoint de dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/dashboards/metrics", headers=headers)
        if response.status_code == 200:
            print("✅ Dashboard métricas OK:", response.json())
        else:
            print("❌ Dashboard métricas falló:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error en endpoint de dashboard:", str(e))

def test_watson_endpoint():
    """Probar endpoint de Watson"""
    print("\n🔍 Probando endpoint de Watson...")
    try:
        response = requests.get(f"{BASE_URL}/watson/status", headers=headers)
        if response.status_code == 200:
            print("✅ Watson status OK:", response.json())
        else:
            print("❌ Watson status falló:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error en endpoint de Watson:", str(e))

def test_reports_endpoint():
    """Probar endpoint de reportes"""
    print("\n🔍 Probando endpoint de reportes...")
    try:
        response = requests.get(f"{BASE_URL}/reports/analytics", headers=headers)
        if response.status_code == 200:
            print("✅ Reportes analytics OK:", response.json())
        else:
            print("❌ Reportes analytics falló:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error en endpoint de reportes:", str(e))

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas de la API UANL Hack")
    print("=" * 50)
    
    test_health_check()
    test_root_endpoint()
    test_operators_endpoint()
    test_dashboard_endpoint()
    test_watson_endpoint()
    test_reports_endpoint()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")
    print("\n📊 Para ver la documentación completa: http://localhost:8000/api/v1/docs")
    print("🌐 Para ver Redoc: http://localhost:8000/api/v1/redoc")

if __name__ == "__main__":
    main()
