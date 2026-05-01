"""
Alarm management service
"""
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys

# Import holiday service
sys.path.insert(0, str(Path(__file__).parent))
from holidays import HolidayService


class AlarmManager:
    """Manages alarm scheduling and triggering"""

    def __init__(self, config_path="config/alarms.json"):
        """Initialize alarm manager"""
        self.config_path = Path(config_path)
        self.alarms = []
        self.holiday_service = HolidayService()
        self.trigger = AlarmTrigger()
        self.load_alarms()

    def load_alarms(self):
        """Load alarms from configuration file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.alarms = json.load(f)
        else:
            self.alarms = []

    def save_alarms(self):
        """Save alarms to configuration file"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.alarms, f, indent=2)

    def add_alarm(self, hour, minute, sound_file=None, enabled=True,
                  skip_weekends=False, skip_holidays=False, weekdays_only=None):
        """
        Add a new alarm

        Args:
            hour: Hour (0-23)
            minute: Minute (0-59)
            sound_file: Sound file to play
            enabled: Whether alarm is enabled
            skip_weekends: Skip Saturday and Sunday
            skip_holidays: Skip public holidays
            weekdays_only: List of weekdays (0=Monday, 6=Sunday) or None for all days
        """
        alarm = {
            "hour": hour,
            "minute": minute,
            "sound": sound_file or "default.mp3",
            "enabled": enabled,
            "skip_weekends": skip_weekends,
            "skip_holidays": skip_holidays,
            "weekdays_only": weekdays_only
        }
        self.alarms.append(alarm)
        self.save_alarms()
        return alarm

    def calculate_sleep_duration(self, alarm_hour, alarm_minute):
        """Calculate hours of sleep until alarm"""
        now = datetime.now()
        alarm_time = now.replace(hour=alarm_hour, minute=alarm_minute, second=0, microsecond=0)

        # If alarm time is earlier than now, it's for tomorrow
        if alarm_time <= now:
            alarm_time += timedelta(days=1)

        duration = alarm_time - now
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60

        return hours, minutes

    def should_alarm_trigger(self, alarm, now=None):
        """
        Check if an alarm should trigger based on time, weekends, and holidays

        Args:
            alarm: Alarm dictionary
            now: Current datetime (defaults to now)

        Returns:
            True if alarm should trigger
        """
        if now is None:
            now = datetime.now()

        # Check if alarm is enabled
        if not alarm.get("enabled", True):
            return False

        # Check time match
        if alarm["hour"] != now.hour or alarm["minute"] != now.minute:
            return False

        # Check weekend skip
        if alarm.get("skip_weekends", False):
            # 5 = Saturday, 6 = Sunday
            if now.weekday() in [5, 6]:
                return False

        # Check specific weekdays
        weekdays_only = alarm.get("weekdays_only")
        if weekdays_only is not None:
            if now.weekday() not in weekdays_only:
                return False

        # Check holiday skip
        if alarm.get("skip_holidays", False):
            if self.holiday_service.is_public_holiday(now):
                return False

        return True

    def check_alarms(self):
        """Check if any alarms should trigger"""
        now = datetime.now()

        triggered = []
        for alarm in self.alarms:
            if self.should_alarm_trigger(alarm, now):
                triggered.append(alarm)

        if triggered and not self.trigger.is_triggered and not self.trigger.check_snooze_expired():
            self.trigger.trigger(triggered[0])

        return triggered

    def is_weekend(self, check_date=None):
        """Check if date is weekend"""
        if check_date is None:
            check_date = datetime.now()
        return check_date.weekday() in [5, 6]

    def is_holiday(self, check_date=None):
        """Check if date is a public holiday"""
        return self.holiday_service.is_public_holiday(check_date)


class AlarmTrigger:
    def __init__(self):
        self.is_triggered = False
        self.triggered_alarm = None
        self.snooze_until = None
        self._sound = None

    def trigger(self, alarm: dict):
        self.is_triggered = True
        self.triggered_alarm = alarm
        try:
            import pygame
            import os
            sound_file = alarm.get("sound", "")
            sounds_dir = Path(__file__).parent.parent.parent / "assets" / "sounds"
            sound_path = sounds_dir / sound_file
            if pygame.mixer.get_init() and sound_path.exists():
                self._sound = pygame.mixer.Sound(str(sound_path))
                self._sound.play(-1)
        except Exception:
            pass

    def snooze(self, minutes: int = 9):
        self.snooze_until = datetime.now() + timedelta(minutes=minutes)
        self.is_triggered = False
        try:
            if self._sound:
                self._sound.stop()
        except Exception:
            pass

    def dismiss(self):
        self.is_triggered = False
        self.triggered_alarm = None
        self.snooze_until = None
        try:
            if self._sound:
                self._sound.stop()
        except Exception:
            pass
        self._sound = None

    def check_snooze_expired(self) -> bool:
        return self.snooze_until is not None and datetime.now() >= self.snooze_until
