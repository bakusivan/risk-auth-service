from typing import List
from ..models.models import LogEntry

class LogCollector:
    def __init__(self):
        self.logs: List[LogEntry] = []

    def add_log(self, log: LogEntry):
        self.logs.append(log)

    def get_logs(self) -> List[LogEntry]:
        return self.logs

    def clear_logs(self):
        self.logs.clear()  # Explicitly clear logs when needed