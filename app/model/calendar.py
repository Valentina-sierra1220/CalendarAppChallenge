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

    def _init_slots(self):
        for h in range(24):
            for m in range(0, 60, 15):
                self.slots[time(h, m)] = None

    def add_event(self, event_id, start_at, end_at):
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot] is not None:
                    slot_not_available_error()
        for slot in self.slots:
            if start_at <= slot < end_at:
                self.slots[slot] = event_id

    def delete_event(self, event_id):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id, start_at, end_at):
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id

class Calendar:
    def __init__(self):
        self.days = {}
        self.events = {}

    def add_event(self, title, description, date_, start_at, end_at):
        if date_ < datetime.now().date():
            date_lower_than_today_error()
        if date_ not in self.days:
            self.days[date_] = Day(date_)
        event = Event(title, description, date_, start_at, end_at)
        self.days[date_].add_event(event.id, start_at, end_at)
        self.events[event.id] = event
        return event.id

    def add_reminder(self, event_id, date_time, type_):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        event.add_reminder(date_time, type_)

    def find_available_slots(self, date_):
        if date_ not in self.days:
            return [time(h, m) for h in range(24) for m in range(0, 60, 15)]
        return [slot for slot, event_id in self.days[date_].slots.items() if event_id is None]

    def update_event(self, event_id, title, description, date_, start_at, end_at):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        is_new_date = event.date_ != date_
        if is_new_date:
            self.delete_event(event_id)
            event = Event(title, description, date_, start_at, end_at)
            event.id = event_id
            self.events[event_id] = event
            if date_ not in self.days:
                self.days[date_] = Day(date_)
            self.days[date_].add_event(event_id, start_at, end_at)

        else:
            event.title = title
            event.description = description
            event.start_at = start_at
            event.end_at = end_at

        for day in self.days.values():
            if not is_new_date and event_id in day.slots.values():
                day.delete_event(event.id)

    def delete_event(self, event_id):
        if event_id not in self.events:
        self.events.pop(event_id)
        for day in self.days.values():
            if event_id in day.slots.values():
                day.delete_event(event_id)







