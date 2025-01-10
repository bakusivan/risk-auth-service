import pytest
from datetime import datetime, timedelta
from src.services.risk_service import RiskService
from src.models.models import LogEntry, RiskValues

@pytest.fixture
def risk_service():
    return RiskService()

@pytest.fixture
def log_data():
    return LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now(),
        login_success=False
    )

def test_process_failed_login(risk_service, log_data):
    # Process a failed login
    risk_service.process_log_chunk(log_data)

    # Verify user risk data
    user_risk = risk_service.get_user_risk("johndoe")
    assert user_risk.is_user_known is True
    assert user_risk.failed_login_count_last_week == 1
    assert user_risk.last_failed_login_date == log_data.date

    # Verify IP risk data
    ip_risk = risk_service.get_ip_risk("192.168.1.10")
    assert ip_risk.is_ip_known is True

    # Verify client risk data
    client_risk = risk_service.get_client_risk("abc123")
    assert client_risk.is_client_known is True

def test_process_successful_login(risk_service):
    # Process a successful login
    log_data_success = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now(),
        login_success=True
    )
    risk_service.process_log_chunk(log_data_success)

    # Verify user risk data
    user_risk = risk_service.get_user_risk("johndoe")
    assert user_risk.is_user_known is True
    assert user_risk.last_successful_login_date == log_data_success.date  # Check that the date matches

    # Verify IP and client data remain consistent
    ip_risk = risk_service.get_ip_risk("192.168.1.10")
    assert ip_risk.is_ip_known is True

    client_risk = risk_service.get_client_risk("abc123")
    assert client_risk.is_client_known is True

def test_get_user_risk_default(risk_service):
    # Verify default risk values for a non-existent user
    user_risk = risk_service.get_user_risk("unknown_user")
    assert user_risk.is_user_known is False
    assert user_risk.failed_login_count_last_week == 0

def test_get_client_risk_default(risk_service):
    # Verify default risk values for a non-existent client
    client_risk = risk_service.get_client_risk("unknown_client")
    assert client_risk.is_client_known is False

def test_get_ip_risk_default(risk_service):
    # Verify default risk values for a non-existent IP
    ip_risk = risk_service.get_ip_risk("0.0.0.0")
    assert ip_risk.is_ip_known is False

def test_ip_internal_check(risk_service):
    # Verify IP internal check
    internal_ip = "10.97.2.15"
    external_ip = "192.168.1.10"

    assert risk_service.is_ip_internal(internal_ip) is True
    assert risk_service.is_ip_internal(external_ip) is False

def test_failed_login_count_within_week(risk_service):
    # Process logs with timestamps within and outside the past week
    log_recent = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now() - timedelta(days=2),
        login_success=False
    )
    log_old = LogEntry(
        username="janedoe",
        device_id="xyz789",
        ip="10.97.2.20",
        date=datetime.now() - timedelta(days=10),
        login_success=False
    )

    risk_service.process_log_chunk(log_recent)
    risk_service.process_log_chunk(log_old)

    # Verify failed login count
    total_failed_logins = risk_service.get_failed_login_count_last_week()
    assert total_failed_logins == 1  # Only recent log counts

def test_process_multiple_logs(risk_service):
    # Process multiple logs
    log_1 = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now(),
        login_success=False
    )
    log_2 = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now() - timedelta(days=3),
        login_success=False
    )
    log_3 = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now() - timedelta(days=8),
        login_success=False
    )

    risk_service.process_log_chunk(log_1)
    risk_service.process_log_chunk(log_2)
    risk_service.process_log_chunk(log_3)

    user_risk = risk_service.get_user_risk("johndoe")
    assert user_risk.failed_login_count_last_week == 2  # Only logs within the last week count

def test_log_data_type_handling(risk_service, mocker):
    from pydantic import BaseModel

    # Test valid string date
    log_string_date = LogEntry(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date=datetime.now().isoformat(),
        login_success=False
    )
    risk_service.process_log_chunk(log_string_date)

    # Mock invalid date handling
    mocker.patch("src.services.risk_service.RiskService.process_log_chunk", side_effect=ValueError("Date format not recognized"))

    # Create an invalid LogEntry bypassing Pydantic validation
    invalid_log_entry = LogEntry.construct(
        username="johndoe",
        device_id="abc123",
        ip="192.168.1.10",
        date="not_a_date",  # Invalid date string
        login_success=False
    )

    with pytest.raises(ValueError, match="Date format not recognized"):
        risk_service.process_log_chunk(invalid_log_entry)

