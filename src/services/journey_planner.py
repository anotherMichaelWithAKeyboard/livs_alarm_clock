from datetime import timedelta
from services.ptv_api import PTVService


class JourneyPlanner:
    def __init__(self, ptv_service=None):
        self.ptv_service = ptv_service

    def find_departures_before(self, route_type, stop_id, arrival_time, journey_minutes, count=3):
        if not self.ptv_service:
            return []

        raw = self.ptv_service.get_departures(route_type, stop_id, max_results=20)

        results = []
        for dep in raw:
            dep_time = dep["time"]
            estimated_arrival = dep_time + timedelta(minutes=journey_minutes)
            if estimated_arrival <= arrival_time:
                entry = dict(dep)
                entry["estimated_arrival"] = estimated_arrival
                entry["journey_minutes"] = journey_minutes
                results.append(entry)

        results.sort(key=lambda d: d["time"], reverse=True)
        return results[:count]

    def find_routes(self, route_configs, arrival_time, count=5):
        all_results = []

        for cfg in route_configs:
            route_type = cfg["route_type"]
            stop_id = cfg["stop_id"]
            journey_minutes = cfg["journey_minutes"]
            label = cfg.get("label", "")

            deps = self.find_departures_before(route_type, stop_id, arrival_time, journey_minutes)
            for dep in deps:
                entry = dict(dep)
                entry["route_label"] = label
                all_results.append(entry)

        all_results.sort(key=lambda d: d["time"])
        return all_results[:count]
