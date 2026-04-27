"""
Australian public holiday service
"""
from datetime import datetime, date
from typing import List, Dict


class HolidayService:
    """Manages Australian public holidays (Victoria specific)"""

    def __init__(self):
        """Initialize holiday service"""
        self.holidays = self._get_holidays()

    def _get_holidays(self) -> Dict[int, List[date]]:
        """
        Get Australian public holidays for Victoria
        Returns dict with year as key and list of holiday dates as value
        """
        # This is a basic implementation - you could enhance this by:
        # - Loading from API
        # - Loading from config file
        # - Auto-calculating movable holidays

        holidays = {
            2024: [
                date(2024, 1, 1),   # New Year's Day
                date(2024, 1, 26),  # Australia Day
                date(2024, 3, 11),  # Labour Day (VIC)
                date(2024, 3, 29),  # Good Friday
                date(2024, 3, 30),  # Saturday before Easter
                date(2024, 3, 31),  # Easter Sunday
                date(2024, 4, 1),   # Easter Monday
                date(2024, 4, 25),  # Anzac Day
                date(2024, 6, 10),  # Queen's Birthday (VIC)
                date(2024, 11, 5),  # Melbourne Cup Day (VIC)
                date(2024, 12, 25), # Christmas Day
                date(2024, 12, 26), # Boxing Day
            ],
            2025: [
                date(2025, 1, 1),   # New Year's Day
                date(2025, 1, 27),  # Australia Day (observed - 26th is Sunday)
                date(2025, 3, 10),  # Labour Day (VIC)
                date(2025, 4, 18),  # Good Friday
                date(2025, 4, 19),  # Saturday before Easter
                date(2025, 4, 20),  # Easter Sunday
                date(2025, 4, 21),  # Easter Monday
                date(2025, 4, 25),  # Anzac Day
                date(2025, 6, 9),   # Queen's Birthday (VIC)
                date(2025, 11, 4),  # Melbourne Cup Day (VIC)
                date(2025, 12, 25), # Christmas Day
                date(2025, 12, 26), # Boxing Day
            ],
            2026: [
                date(2026, 1, 1),   # New Year's Day
                date(2026, 1, 26),  # Australia Day
                date(2026, 3, 9),   # Labour Day (VIC)
                date(2026, 4, 3),   # Good Friday
                date(2026, 4, 4),   # Saturday before Easter
                date(2026, 4, 5),   # Easter Sunday
                date(2026, 4, 6),   # Easter Monday
                date(2026, 4, 25),  # Anzac Day (Saturday)
                date(2026, 6, 8),   # Queen's Birthday (VIC)
                date(2026, 11, 3),  # Melbourne Cup Day (VIC)
                date(2026, 12, 25), # Christmas Day
                date(2026, 12, 26), # Boxing Day (Saturday)
            ]
        }

        return holidays

    def is_public_holiday(self, check_date: datetime = None) -> bool:
        """
        Check if a given date is a public holiday

        Args:
            check_date: Date to check (defaults to today)

        Returns:
            True if the date is a public holiday
        """
        if check_date is None:
            check_date = datetime.now()

        check_date_obj = check_date.date() if isinstance(check_date, datetime) else check_date

        year = check_date_obj.year
        if year not in self.holidays:
            return False

        return check_date_obj in self.holidays[year]

    def get_next_holiday(self, from_date: datetime = None) -> tuple:
        """
        Get the next upcoming holiday

        Args:
            from_date: Start date (defaults to today)

        Returns:
            Tuple of (date, days_until) or (None, None) if no holidays found
        """
        if from_date is None:
            from_date = datetime.now()

        from_date_obj = from_date.date() if isinstance(from_date, datetime) else from_date

        # Check current year and next year
        for year in [from_date_obj.year, from_date_obj.year + 1]:
            if year in self.holidays:
                for holiday in sorted(self.holidays[year]):
                    if holiday > from_date_obj:
                        days_until = (holiday - from_date_obj).days
                        return holiday, days_until

        return None, None

    def get_holiday_name(self, check_date: date) -> str:
        """Get the name of the holiday on a given date"""
        # Simple mapping - could be enhanced
        holiday_names = {
            (1, 1): "New Year's Day",
            (1, 26): "Australia Day",
            (1, 27): "Australia Day",
            (3, 9): "Labour Day",
            (3, 10): "Labour Day",
            (3, 11): "Labour Day",
            (4, 25): "Anzac Day",
            (12, 25): "Christmas Day",
            (12, 26): "Boxing Day",
        }

        # Easter dates vary, so check Melbourne Cup and Queen's Birthday separately
        if check_date.month == 11 and check_date.day <= 7:
            return "Melbourne Cup Day"
        elif check_date.month == 6 and check_date.day <= 14:
            return "Queen's Birthday"
        elif check_date.month in [3, 4] and 15 <= check_date.day <= 25:
            return "Easter"

        return holiday_names.get((check_date.month, check_date.day), "Public Holiday")
