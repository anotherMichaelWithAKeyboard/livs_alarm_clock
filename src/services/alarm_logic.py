from pathlib import Path
from datetime import datetime, timedelta
import json


CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "alarm_config.json"

DEFAULT_CONFIG = {
    "destinations": [],
    "starting_points": [{"name": "Home", "address": ""}],
    "fluffer_activities": [],
    "plan": {
        "destination": None,
        "start_location": "Home",
        "arrival_time": "08:00",
        "transport_mode": "public_transport",
        "journey_minutes": 0,
        "selected_departure": None,
        "fluffer_selected": [],
        "snooze_count": 0,
        "snooze_duration": 9,
        "alarm_time": None,
    },
}


class AlarmConfig:
    def __init__(self, config_path=None):
        self._path = Path(config_path) if config_path else CONFIG_PATH
        self._data = {}
        self._load()

    def _load(self):
        if self._path.exists():
            with open(self._path, "r") as f:
                self._data = json.load(f)
        else:
            import copy
            self._data = copy.deepcopy(DEFAULT_CONFIG)

    def save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=2)

    @property
    def destinations(self):
        return sorted(self._data.get("destinations", []), key=lambda d: d.get("count", 0), reverse=True)

    @property
    def fluffer_activities(self):
        return self._data.get("fluffer_activities", [])

    @property
    def starting_points(self):
        return self._data.get("starting_points", [])

    @property
    def plan(self):
        return self._data.get("plan", {})

    def add_destination(self, name, address):
        for dest in self._data.setdefault("destinations", []):
            if dest["name"] == name:
                dest["address"] = address
                self.save()
                return
        self._data["destinations"].append({"name": name, "address": address, "count": 0})
        self.save()

    def use_destination(self, name):
        for dest in self._data.get("destinations", []):
            if dest["name"] == name:
                dest["count"] = dest.get("count", 0) + 1
                self.save()
                return

    def remove_destination(self, name):
        self._data["destinations"] = [
            d for d in self._data.get("destinations", []) if d["name"] != name
        ]
        self.save()

    def add_starting_point(self, name, address):
        for sp in self._data.setdefault("starting_points", []):
            if sp["name"] == name:
                sp["address"] = address
                self.save()
                return
        self._data["starting_points"].append({"name": name, "address": address})
        self.save()

    def add_route_config(self, route_type, stop_id, journey_minutes, label=""):
        plan = self._data.setdefault("plan", {})
        configs = plan.setdefault("route_configs", [])
        for cfg in configs:
            if cfg.get("stop_id") == stop_id and cfg.get("route_type") == route_type:
                cfg["journey_minutes"] = journey_minutes
                cfg["label"] = label
                self.save()
                return
        configs.append({
            "route_type": route_type,
            "stop_id": stop_id,
            "journey_minutes": journey_minutes,
            "label": label,
        })
        self.save()

    def update_destination(self, old_name, new_name, new_address):
        for dest in self._data.get("destinations", []):
            if dest["name"] == old_name:
                dest["name"] = new_name
                dest["address"] = new_address
                self.save()
                return

    def update_starting_point(self, old_name, new_name, new_address):
        for sp in self._data.get("starting_points", []):
            if sp["name"] == old_name:
                sp["name"] = new_name
                sp["address"] = new_address
                self.save()
                return

    def add_activity(self, name, minutes):
        for act in self._data.setdefault("fluffer_activities", []):
            if act["name"] == name:
                act["minutes"] = minutes
                self.save()
                return
        self._data["fluffer_activities"].append({"name": name, "minutes": minutes})
        self.save()

    def remove_activity(self, name):
        self._data["fluffer_activities"] = [
            a for a in self._data.get("fluffer_activities", []) if a["name"] != name
        ]
        self.save()

    def total_fluffer_minutes(self, selected_names=None):
        activities = self._data.get("fluffer_activities", [])
        if selected_names is None:
            return sum(a.get("minutes", 0) for a in activities)
        name_set = set(selected_names)
        return sum(a.get("minutes", 0) for a in activities if a["name"] in name_set)

    def update_plan(self, **kwargs):
        self._data.setdefault("plan", {}).update(kwargs)
        self.save()


class AlarmCalculator:
    @staticmethod
    def departure_from_arrival(arrival: datetime, journey_minutes: int) -> datetime:
        return arrival - timedelta(minutes=journey_minutes)

    @staticmethod
    def alarm_from_departure(
        departure: datetime,
        fluffer_minutes: int,
        snooze_count: int = 0,
        snooze_duration: int = 9,
    ) -> datetime:
        snooze_buffer = snooze_count * snooze_duration
        return departure - timedelta(minutes=fluffer_minutes + snooze_buffer)

    @staticmethod
    def sleep_duration(alarm: datetime) -> tuple:
        now = datetime.now()
        alarm_naive = alarm.replace(tzinfo=None) if alarm.tzinfo else alarm
        target = now.replace(
            hour=alarm_naive.hour,
            minute=alarm_naive.minute,
            second=0,
            microsecond=0,
        )
        if target <= now:
            target += timedelta(days=1)
        delta = target - now
        hours = int(delta.total_seconds()) // 3600
        minutes = (int(delta.total_seconds()) % 3600) // 60
        return hours, minutes

    @staticmethod
    def full_summary(
        arrival: datetime,
        journey_minutes: int,
        fluffer_minutes: int,
        snooze_count: int = 0,
        snooze_duration: int = 9,
    ) -> dict:
        departure = AlarmCalculator.departure_from_arrival(arrival, journey_minutes)
        alarm = AlarmCalculator.alarm_from_departure(
            departure, fluffer_minutes, snooze_count, snooze_duration
        )
        sleep_hours, sleep_mins = AlarmCalculator.sleep_duration(alarm)
        return {
            "departure_time": departure,
            "alarm_time": alarm,
            "sleep_hours": sleep_hours,
            "sleep_minutes": sleep_mins,
            "fluffer_minutes": fluffer_minutes,
            "snooze_buffer_minutes": snooze_count * snooze_duration,
        }
