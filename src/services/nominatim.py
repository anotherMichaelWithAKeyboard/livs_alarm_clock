"""
Nominatim (OpenStreetMap) address autocomplete — free, no API key required.
Rate limit: 1 req/sec. Fine for infrequent use.
"""
import json
import threading
import urllib.parse
import urllib.request

_BASE = "https://nominatim.openstreetmap.org/search"
_UA   = "LivsAlarmClock/1.0 (raspberry-pi home project)"

_STATE_ABBR = {
    "Victoria": "VIC", "New South Wales": "NSW", "Queensland": "QLD",
    "Western Australia": "WA", "South Australia": "SA", "Tasmania": "TAS",
    "Australian Capital Territory": "ACT", "Northern Territory": "NT",
}


def _format(result: dict) -> str:
    """Turn a Nominatim result into a short readable address."""
    addr = result.get("address", {})
    parts = []

    num  = addr.get("house_number", "")
    road = addr.get("road", "")
    if num and road:
        parts.append(f"{num} {road}")
    elif road:
        parts.append(road)

    suburb = (addr.get("suburb") or addr.get("village")
              or addr.get("town") or addr.get("city_district") or "")
    if suburb:
        parts.append(suburb)

    state    = _STATE_ABBR.get(addr.get("state", ""), "")
    postcode = addr.get("postcode", "")
    suffix   = f"{state} {postcode}".strip()
    if suffix:
        parts.append(suffix)

    return ", ".join(parts) if parts else result.get("display_name", "")


class NominatimGeocoder:
    """Thread-safe fire-and-forget geocoder."""

    def search_async(self, query: str, callback, country: str = "au"):
        """
        Fetch address suggestions in a daemon thread.
        callback([str, ...]) is called on the thread (not the main thread).
        The list may be empty on error or no results.
        """
        def _fetch():
            try:
                params = urllib.parse.urlencode({
                    "q": query,
                    "format": "json",
                    "addressdetails": "1",
                    "countrycodes": country,
                    "limit": "5",
                })
                req = urllib.request.Request(
                    f"{_BASE}?{params}",
                    headers={"User-Agent": _UA},
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                results = [_format(r) for r in data if r.get("address")]
                # Deduplicate while preserving order
                seen, unique = set(), []
                for r in results:
                    if r and r not in seen:
                        seen.add(r)
                        unique.append(r)
                callback(unique)
            except Exception:
                callback([])

        threading.Thread(target=_fetch, daemon=True).start()
