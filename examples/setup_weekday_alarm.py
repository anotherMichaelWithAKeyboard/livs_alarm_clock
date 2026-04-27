#!/usr/bin/env python3
"""
Example: Setting up a weekday-only alarm that skips weekends and holidays
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.alarm_manager import AlarmManager


def main():
    """Set up weekday alarm"""
    alarm_mgr = AlarmManager()

    # Example 1: Skip weekends and holidays
    print("Setting up alarm for 6:30 AM (weekdays only, skip holidays)...")
    alarm_mgr.add_alarm(
        hour=6,
        minute=30,
        sound_file="morning.mp3",
        skip_weekends=True,
        skip_holidays=True
    )

    # Example 2: Monday to Friday only (more explicit)
    print("Setting up alarm for 7:00 AM (Mon-Fri only)...")
    alarm_mgr.add_alarm(
        hour=7,
        minute=0,
        sound_file="beep.mp3",
        weekdays_only=[0, 1, 2, 3, 4]  # 0=Monday, 6=Sunday
    )

    # Example 3: Weekend-only alarm
    print("Setting up alarm for 9:00 AM (weekends only)...")
    alarm_mgr.add_alarm(
        hour=9,
        minute=0,
        sound_file="gentle.mp3",
        weekdays_only=[5, 6]  # Saturday and Sunday
    )

    print("\n✓ Alarms configured successfully!")
    print(f"\nTotal alarms: {len(alarm_mgr.alarms)}")

    # Show alarm details
    print("\nConfigured alarms:")
    for i, alarm in enumerate(alarm_mgr.alarms, 1):
        time_str = f"{alarm['hour']:02d}:{alarm['minute']:02d}"
        print(f"\n{i}. {time_str}")
        if alarm.get('skip_weekends'):
            print("   - Skips weekends")
        if alarm.get('skip_holidays'):
            print("   - Skips public holidays")
        if alarm.get('weekdays_only'):
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            active_days = [days[d] for d in alarm['weekdays_only']]
            print(f"   - Active days: {', '.join(active_days)}")

    # Test weekend/holiday detection
    print("\n\nTesting detection:")
    print(f"Is today a weekend? {alarm_mgr.is_weekend()}")
    print(f"Is today a holiday? {alarm_mgr.is_holiday()}")

    if alarm_mgr.is_holiday():
        from datetime import datetime
        holiday_name = alarm_mgr.holiday_service.get_holiday_name(datetime.now().date())
        print(f"Holiday: {holiday_name}")

    # Check next holiday
    next_holiday, days_until = alarm_mgr.holiday_service.get_next_holiday()
    if next_holiday:
        print(f"\nNext holiday: {next_holiday} ({days_until} days away)")


if __name__ == "__main__":
    main()
