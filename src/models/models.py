from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class LogEntry(BaseModel):
    username: str
    device_id: str
    ip: str
    date: datetime
    login_success: bool

class RiskValues(BaseModel):
    is_user_known: bool
    is_client_known: bool
    is_ip_known: bool
    is_ip_internal: bool
    last_successful_login_date: Optional[datetime] = None
    last_failed_login_date: Optional[datetime] = None
    failed_login_count_last_week: int = 0
