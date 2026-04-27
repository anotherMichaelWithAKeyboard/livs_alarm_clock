#!/usr/bin/env python3
"""
Example: Finding PTV stop IDs for your commute
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.ptv_api import PTVService


def main():
    """Find PTV stop IDs"""
    print("PTV Stop ID Finder")
    print("=" * 50)
    print()

    # Get API credentials
    dev_id = input("Enter your PTV Developer ID: ").strip()
    api_key = input("Enter your PTV API Key: ").strip()

    if not dev_id or not api_key:
        print("\n❌ Error: Both Developer ID and API Key are required")
        print("\nGet your credentials from:")
        print("https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/")
        return

    ptv = PTVService(dev_id, api_key)

    # Search for stops
    print("\n" + "=" * 50)
    print("Search for your stops")
    print("=" * 50)

    while True:
        print("\nRoute types:")
        print("  0 = Train")
        print("  1 = Tram")
        print("  2 = Bus")
        print()

        search_term = input("Enter stop name (or 'quit' to exit): ").strip()
        if search_term.lower() in ['quit', 'exit', 'q']:
            break

        route_type = input("Enter route type (0/1/2) or press Enter for all: ").strip()

        route_types = None
        if route_type:
            try:
                route_types = [int(route_type)]
            except ValueError:
                print("Invalid route type. Searching all types...")

        print(f"\nSearching for '{search_term}'...")
        stops = ptv.search_stops(search_term, route_types)

        if not stops:
            print("❌ No stops found. Try a different search term.")
            continue

        print(f"\n✓ Found {len(stops)} stops:\n")

        for i, stop in enumerate(stops[:10], 1):  # Show max 10 results
            route_type_name = {0: 'Train', 1: 'Tram', 2: 'Bus'}.get(stop.get('route_type'), 'Unknown')
            print(f"{i}. {stop['stop_name']}")
            print(f"   ID: {stop['stop_id']}")
            print(f"   Type: {route_type_name}")
            print(f"   Suburb: {stop.get('stop_suburb', 'N/A')}")
            print()

    print("\nConfiguration example:")
    print("=" * 50)
    print("""
Add these to your config/settings.json:

{
  "ptv": {
    "devId": "YOUR_DEV_ID",
    "apiKey": "YOUR_API_KEY",
    "homeStopId": 1071,  // Replace with your home stop ID
    "homeRouteType": 0,   // 0=train, 1=tram, 2=bus
    "workStopId": 1181,   // Replace with your work stop ID
    "workRouteType": 0
  }
}
    """)


if __name__ == "__main__":
    main()
