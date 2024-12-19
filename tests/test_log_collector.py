import pytest
from datetime import date
from src.services.log_collector import LogCollector
from src.models.models import LogEntry

# Test the LogCollector class
@pytest.fixture
def log_collector():
    return LogCollector()

def test_add_log(log_collector):
    # Create a log entry
    log = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=date(2024, 12, 19),
        login_success=True
    )
    
    # Add the log to the log_collector
    log_collector.add_log(log)
    
    # Check that the log has been added
    assert len(log_collector.get_logs()) == 1
    assert log_collector.get_logs()[0] == log

def test_get_logs(log_collector):
    # Add multiple logs
    log1 = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=date(2024, 12, 19),
        login_success=True
    )
    
    log2 = LogEntry(
        username="janedoe",
        device_id="xyz456",
        ip="192.168.1.11",
        date=date(2024, 12, 20),
        login_success=False
    )
    
    log_collector.add_log(log1)
    log_collector.add_log(log2)
    
    # Check that both logs are stored
    logs = log_collector.get_logs()
    assert len(logs) == 2
    assert logs[0] == log1
    assert logs[1] == log2
