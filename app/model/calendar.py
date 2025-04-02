from dataclasses import dataclass, field
from datetime import datetime, date, time
from app.services.util import generate_unique_id, reminder_not_found_error, slot_not_available_error, event_not_found_error, date_lower_than_today_error
@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"
    date_time: datetime
    type: str = EMAIL

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)


    def add_reminder(self, date_time, type_=Reminder.EMAIL):
        self.reminders.append(Reminder(date_time, type_))

    def delete_reminder(self, reminder_index):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

    def __str__(self):
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"


class Day:
    def __init__(self, date_):
        self.date_ = date_
        self.slots = {}
        self._init_slots()







