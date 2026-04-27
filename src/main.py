#!/usr/bin/env python3
"""
Custom Alarm Clock - Main Application
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.clock_display import ClockApp


def main():
    """Main entry point for the alarm clock application"""
    app = ClockApp()
    app.run()


if __name__ == "__main__":
    main()
