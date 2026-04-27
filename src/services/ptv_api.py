"""
PTV (Public Transport Victoria) API service for train and tram schedules
"""
import requests
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class PTVService:
    """
    Service for fetching train and tram schedules from PTV API

    To use this service:
    1. Get API credentials from: https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/
    2. Add dev_id and api_key to config/settings.json
    """

    def __init__(self, dev_id=None, api_key=None):
        """
        Initialize PTV service

        Args:
            dev_id: Developer ID from PTV
            api_key: API key from PTV
        """
        self.dev_id = dev_id
        self.api_key = api_key
        self.base_url = "https://timetableapi.ptv.vic.gov.au"

        # Route types
        self.TRAIN = 0
        self.TRAM = 1
        self.BUS = 2

    def _generate_signature(self, request_path: str) -> str:
        """
        Generate HMAC-SHA1 signature for PTV API request

        Args:
            request_path: The request path including query params

        Returns:
            The signature string
        """
        if not self.api_key:
            return ""

        signature = hmac.new(
            self.api_key.encode('utf-8'),
            request_path.encode('utf-8'),
            hashlib.sha1
        ).hexdigest().upper()

        return signature

    def _make_request(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """
        Make authenticated request to PTV API

        Args:
            endpoint: API endpoint (e.g., "/v3/stops/route_type/0")
            params: Query parameters

        Returns:
            JSON response or None on error
        """
        if not self.dev_id or not self.api_key:
            print("PTV API credentials not configured")
            return None

        # Add developer ID to params
        if params is None:
            params = {}
        params['devid'] = self.dev_id

        # Build query string
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        request_path = f"{endpoint}?{query_string}"

        # Generate signature
        signature = self._generate_signature(request_path)

        # Build full URL
        url = f"{self.base_url}{request_path}&signature={signature}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"PTV API error: {e}")
            return None

    def search_stops(self, search_term: str, route_types: List[int] = None) -> List[Dict]:
        """
        Search for stops by name

        Args:
            search_term: Stop name to search for
            route_types: List of route types to filter (0=train, 1=tram, 2=bus)

        Returns:
            List of matching stops
        """
        params = {'route_types': ','.join(map(str, route_types))} if route_types else {}

        result = self._make_request(f"/v3/search/{search_term}", params)

        if result and 'stops' in result:
            return result['stops']
        return []

    def get_departures(self, route_type: int, stop_id: int, route_id: int = None,
                       max_results: int = 5) -> List[Dict]:
        """
        Get upcoming departures from a stop

        Args:
            route_type: Type of transport (0=train, 1=tram, 2=bus)
            stop_id: Stop ID
            route_id: Optional route ID to filter results
            max_results: Maximum number of results

        Returns:
            List of departures with times and destinations
        """
        endpoint = f"/v3/departures/route_type/{route_type}/stop/{stop_id}"

        params = {
            'max_results': max_results,
            'expand': 'route,run,direction'
        }

        if route_id:
            params['route_id'] = route_id

        result = self._make_request(endpoint, params)

        if not result or 'departures' not in result:
            return []

        departures = []
        for dep in result['departures']:
            # Parse scheduled departure time
            scheduled_time = dep.get('scheduled_departure_utc')
            estimated_time = dep.get('estimated_departure_utc')

            # Use estimated time if available, otherwise scheduled
            departure_time_str = estimated_time or scheduled_time

            if departure_time_str:
                departure_time = datetime.fromisoformat(departure_time_str.replace('Z', '+00:00'))

                # Convert to local time
                local_time = departure_time.astimezone()

                # Calculate minutes until departure
                now = datetime.now(departure_time.tzinfo)
                minutes_until = int((departure_time - now).total_seconds() / 60)

                departures.append({
                    'time': local_time,
                    'minutes_until': minutes_until,
                    'direction_name': dep.get('direction_name', 'Unknown'),
                    'route_number': dep.get('route_number', ''),
                    'scheduled_time': scheduled_time,
                    'estimated_time': estimated_time,
                    'at_platform': dep.get('at_platform', False),
                    'platform_number': dep.get('platform_number', '')
                })

        return sorted(departures, key=lambda x: x['time'])

    def get_route_id(self, route_name: str, route_type: int) -> Optional[int]:
        """
        Get route ID from route name

        Args:
            route_name: Name or number of the route
            route_type: Type of transport (0=train, 1=tram, 2=bus)

        Returns:
            Route ID or None if not found
        """
        result = self._make_request(f"/v3/routes", {'route_types': route_type})

        if result and 'routes' in result:
            for route in result['routes']:
                if (route.get('route_name', '').lower() == route_name.lower() or
                    route.get('route_number', '') == route_name):
                    return route['route_id']

        return None


class CommuteTracker:
    """Track and display commute information"""

    def __init__(self, ptv_service: PTVService):
        """
        Initialize commute tracker

        Args:
            ptv_service: Configured PTV service instance
        """
        self.ptv = ptv_service
        self.home_stop = None
        self.work_stop = None
        self.home_route_type = None
        self.work_route_type = None

    def configure_commute(self, home_stop_id: int, home_route_type: int,
                         work_stop_id: int, work_route_type: int):
        """
        Configure commute stops

        Args:
            home_stop_id: Stop ID near home
            home_route_type: Route type from home (0=train, 1=tram)
            work_stop_id: Stop ID near work
            work_route_type: Route type from work
        """
        self.home_stop = home_stop_id
        self.home_route_type = home_route_type
        self.work_stop = work_stop_id
        self.work_route_type = work_route_type

    def get_morning_departures(self, max_results: int = 3) -> List[Dict]:
        """Get departures from home stop (morning commute)"""
        if not self.home_stop:
            return []

        return self.ptv.get_departures(
            self.home_route_type,
            self.home_stop,
            max_results=max_results
        )

    def get_evening_departures(self, max_results: int = 3) -> List[Dict]:
        """Get departures from work stop (evening commute)"""
        if not self.work_stop:
            return []

        return self.ptv.get_departures(
            self.work_route_type,
            self.work_stop,
            max_results=max_results
        )

    def get_next_departure(self, is_morning: bool = True) -> Optional[Dict]:
        """
        Get the next departure for commute

        Args:
            is_morning: True for morning commute, False for evening

        Returns:
            Next departure info or None
        """
        departures = self.get_morning_departures(1) if is_morning else self.get_evening_departures(1)

        return departures[0] if departures else None
