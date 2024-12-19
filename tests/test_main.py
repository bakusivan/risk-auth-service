import pytest
from datetime import date
from fastapi.testclient import TestClient
from src.main import app  # Ensure main.py is in the same directory or package
from src.models.models import LogEntry
from src.services.log_collector import LogCollector

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def reset_log_collector():
    # Create a new LogCollector instance before each test
    from src.main import log_collector  # Import the shared instance
    log_collector.logs.clear()  # Clear logs globally
    return log_collector

def test_health(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"message": "Health OK!"}

def test_create_log(client):
    log_data = {
        "user": "johndoe1",
        "device_id": "abc123",
        "ip_address": "192.168.1.10",
        "date": "2024-12-19",
        "login_success": True
    }
    
    # POST request to add log
    response = client.post("/log/", json=log_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Log entry added successfully!"}

    # GET request to check the log was added
    response = client.get("/logs/")
    assert response.status_code == 200
    logs = response.json()
    
    # Check that the log is present
    assert len(logs) == 1
    assert logs[0]["user"] == "johndoe1"
    assert logs[0]["device_id"] == "abc123"
    assert logs[0]["ip_address"] == "192.168.1.10"
    assert logs[0]["date"] == "2024-12-19"
    assert logs[0]["login_success"] == True

def test_get_logs(client, reset_log_collector):
    log_collector = reset_log_collector
    log_data1 = {
        "user": "johndoe",
        "device_id": "abc123",
        "ip_address": "192.168.1.10",
        "date": "2024-12-19",
        "login_success": True
    }
    log_data2 = {
        "user": "janedoe",
        "device_id": "xyz456",
        "ip_address": "192.168.1.11",
        "date": "2024-12-20",
        "login_success": False
    }
    
    # Add two logs
    client.post("/log/", json=log_data1)
    client.post("/log/", json=log_data2)

    # GET request to fetch logs
    response = client.get("/logs/")
    assert response.status_code == 200
    logs = response.json()

    assert len(logs) == 2
    assert logs[0]["user"] == "johndoe"
    assert logs[1]["user"] == "janedoe"
