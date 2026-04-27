"""
Configuration loader utility
"""
import json
from pathlib import Path


class ConfigLoader:
    """Loads and manages application configuration"""

    def __init__(self, config_dir="config"):
        """Initialize config loader"""
        self.config_dir = Path(config_dir)
        self.settings = None
        self.load_settings()

    def load_settings(self):
        """Load settings from config file"""
        settings_file = self.config_dir / "settings.json"

        if settings_file.exists():
            with open(settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            # Default settings
            self.settings = {
                "display": {
                    "width": 800,
                    "height": 480,
                    "fullscreen": False,
                    "brightness": 100
                },
                "dimMode": {
                    "enabled": True,
                    "startTime": "22:00",
                    "endTime": "06:00",
                    "brightness": 20
                },
                "timezone": "Australia/Melbourne"
            }

        return self.settings

    def save_settings(self):
        """Save current settings to file"""
        settings_file = self.config_dir / "settings.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key_path, default=None):
        """
        Get a configuration value using dot notation
        Example: get("display.width") returns settings["display"]["width"]
        """
        keys = key_path.split('.')
        value = self.settings

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path, value):
        """
        Set a configuration value using dot notation
        Example: set("display.width", 1024)
        """
        keys = key_path.split('.')
        current = self.settings

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        self.save_settings()
