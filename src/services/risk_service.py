import ipaddress
from datetime import datetime, timedelta
from typing import Dict
from ..models.models import RiskValues, LogEntry

class RiskService:
    def __init__(self):
        self.user_data: Dict[str, RiskValues] = {}
        self.client_data: Dict[str, RiskValues] = {}
        self.ip_data: Dict[str, RiskValues] = {}

    def process_log_chunk(self, log_chunk: LogEntry) -> None:
        # Ensure the log date is a datetime object (if it's a date, we convert it to datetime at 00:00:00)
        if isinstance(log_chunk.date, datetime):
            log_chunk_date = log_chunk.date
        elif isinstance(log_chunk.date, str):
            # If it's a string, convert it to a datetime object
            try:
                log_chunk_date = datetime.fromisoformat(log_chunk.date)
            except ValueError:
                raise ValueError("Date format not recognized")
        else:
            raise ValueError("Date format not recognized")
        
        # Calculate the timestamp for one week ago
        one_week_ago = datetime.now() - timedelta(days=7)

        username = log_chunk.username
        device_id = log_chunk.device_id
        ip = log_chunk.ip

        # Process user data (initialize with all required fields)
        user_risk = self.user_data.get(username, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=self.is_ip_internal(ip),
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))
        user_risk.is_user_known = True

        # Process client data (initialize with all required fields)
        client_risk = self.client_data.get(device_id, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=self.is_ip_internal(ip),
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))
        client_risk.is_client_known = True

        # Process IP data (initialize with all required fields)
        ip_risk = self.ip_data.get(ip, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=self.is_ip_internal(ip),
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))
        ip_risk.is_ip_known = True

        # If the log is within the last week
        if log_chunk_date >= one_week_ago:
            if not log_chunk.login_success:
                # If login failed, increment the failed login count for the user
                user_risk = self.user_data.get(log_chunk.username)
                
                if user_risk:
                    user_risk.failed_login_count_last_week += 1
                    user_risk.last_failed_login_date = log_chunk_date  # Update last failed login date
                else:
                    # Initialize user risk data if it doesn't exist
                    user_risk = RiskValues(
                        is_user_known=True,  # Make sure to set required fields
                        is_client_known=False,
                        is_ip_known=False,
                        is_ip_internal=self.is_ip_internal(ip),
                        last_successful_login_date=None,
                        last_failed_login_date=log_chunk_date,
                        failed_login_count_last_week=1
                    )
                    self.user_data[log_chunk.username] = user_risk
        
        # Save updated risk values
        self.user_data[username] = user_risk
        self.client_data[device_id] = client_risk
        self.ip_data[ip] = ip_risk

    def get_user_risk(self, username: str) -> RiskValues:
        return self.user_data.get(username, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=False,
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))

    def get_client_risk(self, device_id: str) -> RiskValues:
        return self.client_data.get(device_id, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=False,
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))

    def get_ip_risk(self, ip: str) -> RiskValues:
        return self.ip_data.get(ip, RiskValues(
            is_user_known=False,
            is_client_known=False,
            is_ip_known=False,
            is_ip_internal=False,
            last_successful_login_date=None,
            last_failed_login_date=None,
            failed_login_count_last_week=0
        ))

    def is_ip_internal(self, ip: str) -> bool:
        internal_subnet = ipaddress.ip_network("10.97.2.0/24")
        try:
            return ipaddress.ip_address(ip) in internal_subnet
        except ValueError:
            return False  # Handle invalid IP formats gracefully

    def get_failed_login_count_last_week(self):
        total_failed_login_count = 0
        one_week_ago = datetime.now() - timedelta(days=7)

        # Summing the failed login count for all users within the last week
        for user_risk in self.user_data.values():
            if user_risk.last_failed_login_date and user_risk.last_failed_login_date >= one_week_ago:
                total_failed_login_count += user_risk.failed_login_count_last_week

        return total_failed_login_count
