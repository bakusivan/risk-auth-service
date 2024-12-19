# models.py
from pydantic import BaseModel
from datetime import date

class LogEntry(BaseModel):
    user: str
    device_id: str
    ip_address: str
    date: date
    login_success: bool
