"""
Tests for alarm manager
"""
import unittest
from pathlib import Path
import sys
import tempfile
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.alarm_manager import AlarmManager


class TestAlarmManager(unittest.TestCase):
    """Test cases for AlarmManager"""

    def setUp(self):
        """Set up test fixtures"""
        # Use temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "alarms.json"
        self.manager = AlarmManager(config_path=self.config_path)

    def test_add_alarm(self):
        """Test adding an alarm"""
        alarm = self.manager.add_alarm(7, 30, "morning.mp3")

        self.assertEqual(alarm["hour"], 7)
        self.assertEqual(alarm["minute"], 30)
        self.assertEqual(alarm["sound"], "morning.mp3")
        self.assertTrue(alarm["enabled"])

    def test_calculate_sleep_duration(self):
        """Test sleep duration calculation"""
        # This will depend on current time, so just check it returns valid values
        hours, minutes = self.manager.calculate_sleep_duration(7, 30)

        self.assertIsInstance(hours, int)
        self.assertIsInstance(minutes, int)
        self.assertGreaterEqual(hours, 0)
        self.assertGreaterEqual(minutes, 0)
        self.assertLess(minutes, 60)

    def test_save_and_load_alarms(self):
        """Test saving and loading alarms"""
        self.manager.add_alarm(8, 0, "test.mp3")
        self.manager.add_alarm(9, 15, "test2.mp3")

        # Create new manager with same config file
        new_manager = AlarmManager(config_path=self.config_path)

        self.assertEqual(len(new_manager.alarms), 2)
        self.assertEqual(new_manager.alarms[0]["hour"], 8)
        self.assertEqual(new_manager.alarms[1]["hour"], 9)


if __name__ == "__main__":
    unittest.main()
