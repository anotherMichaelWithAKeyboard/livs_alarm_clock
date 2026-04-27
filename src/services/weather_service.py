"""
Weather forecast service using BOM/WillyWeather API
"""
import requests
from datetime import datetime


class WeatherService:
    """Handles weather forecast fetching and cycling condition checks"""

    def __init__(self, api_key=None, location="Melbourne"):
        """Initialize weather service"""
        self.api_key = api_key
        self.location = location
        self.forecast_data = None

    def fetch_forecast(self):
        """Fetch weather forecast from API"""
        # TODO: Implement actual API calls to BOM or WillyWeather
        # This is a placeholder structure

        # Example placeholder data structure
        self.forecast_data = {
            "daily": [
                {
                    "date": "2024-04-26",
                    "temp_max": 22,
                    "temp_min": 14,
                    "rain_chance": 20,
                    "rain_amount": 0.2,
                    "conditions": "Partly Cloudy"
                }
            ]
        }
        return self.forecast_data

    def can_ride_to_work(self, date=None):
        """
        Check if cycling conditions are good for morning ride (6am-8am)
        Returns True if no rain, not too cold, good cycling conditions
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if not self.forecast_data:
            self.fetch_forecast()

        # Find the forecast for the specified date
        day_forecast = next(
            (d for d in self.forecast_data.get("daily", []) if d["date"] == date),
            None
        )

        if not day_forecast:
            return None

        # Criteria for "can ride"
        # - Temperature min above 10°C
        # - Rain chance below 30%
        # - Rain amount below 1mm

        can_ride = (
            day_forecast["temp_min"] >= 10 and
            day_forecast["rain_chance"] < 30 and
            day_forecast["rain_amount"] < 1.0
        )

        return can_ride

    def can_ride_from_work(self, date=None):
        """
        Check if cycling conditions are good for evening ride (4pm-6pm)
        Returns True if no rain, not too cold, good cycling conditions
        """
        # Similar logic to morning, but might consider different criteria
        # For now, using the same logic
        return self.can_ride_to_work(date)

    def get_weekly_forecast(self):
        """Get forecast for the upcoming week"""
        if not self.forecast_data:
            self.fetch_forecast()

        return self.forecast_data.get("daily", [])
