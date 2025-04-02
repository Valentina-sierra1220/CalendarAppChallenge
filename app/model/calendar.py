from dataclasses import dataclass
from datetime import datetime
@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"
    date_time: datetime

