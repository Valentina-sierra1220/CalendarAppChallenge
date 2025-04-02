from dataclasses import dataclass
from datetime import datetime
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





