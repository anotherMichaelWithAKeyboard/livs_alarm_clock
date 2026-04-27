# New Features Guide

This document explains the newly implemented features for the custom alarm clock.

## 1. Seasonal Themes

The alarm clock automatically adjusts its color scheme based on the Australian seasons:

### Seasons
- **Summer** (Dec, Jan, Feb): Deep blue with warm yellow/orange accents
- **Autumn** (Mar, Apr, May): Dark brown with burnt orange and gold
- **Winter** (Jun, Jul, Aug): Dark blue-gray with cool blue tones
- **Spring** (Sep, Oct, Nov): Dark green-gray with fresh green and pink

### How It Works
- Theme automatically updates based on the current date
- Colors change hourly to reflect seasonal transitions
- Current season is displayed in the top-right corner

### Manual Configuration
Themes are defined in `src/ui/themes.py`. You can customize colors by editing the theme dictionaries.

---

## 2. Photo Frame Mode

The alarm clock enters photo frame mode after a period of inactivity, displaying your personal photos.

### Setup
1. Add photos to `assets/photos/` directory
2. Supported formats: JPG, PNG, BMP, GIF
3. Configure idle timeout in `config/settings.json`:

```json
{
  "photoFrame": {
    "enabled": true,
    "idleTimeout": 60,  // seconds before entering photo mode
    "photoChangeInterval": 10,  // seconds between photos
    "photoDir": "assets/photos"
  }
}
```

### Features
- Photos automatically scale to fit screen
- Maintains aspect ratio
- Displays in random order
- Changes photo every 10 seconds
- Any interaction returns to clock display

---

## 3. Weekend/Holiday Detection

Alarms can now automatically skip weekends and public holidays to prevent accidental early wake-ups.

### Victorian Public Holidays Supported
- New Year's Day
- Australia Day
- Labour Day
- Easter (Good Friday, Saturday, Sunday, Monday)
- Anzac Day
- Queen's Birthday
- Melbourne Cup Day
- Christmas Day
- Boxing Day

### Setting Up Skip-Weekend Alarms

#### Example: Weekday-only alarm at 6:30am
```python
from services.alarm_manager import AlarmManager

alarm_mgr = AlarmManager()

# Skip weekends
alarm_mgr.add_alarm(
    hour=6,
    minute=30,
    skip_weekends=True,
    skip_holidays=True
)
```

#### Example: Monday-Friday only alarm
```python
# Weekdays only (0=Monday, 4=Friday)
alarm_mgr.add_alarm(
    hour=7,
    minute=0,
    weekdays_only=[0, 1, 2, 3, 4]
)
```

### Alarm Configuration
Alarms are stored in `config/alarms.json` with these fields:
```json
{
  "hour": 6,
  "minute": 30,
  "sound": "morning.mp3",
  "enabled": true,
  "skip_weekends": true,
  "skip_holidays": true,
  "weekdays_only": [0, 1, 2, 3, 4]
}
```

### Holiday Display
- Weekend indicator shows "Weekend" in top-left
- Holiday indicator shows "🎉 Holiday Name" in top-left

---

## 4. Commute Planner (Train/Tram Schedules)

Displays real-time train and tram departures using the PTV (Public Transport Victoria) API.

### Setup

#### Step 1: Get PTV API Credentials
1. Visit: https://www.ptv.vic.gov.au/footer/data-and-reporting/datasets/ptv-timetable-api/
2. Register for API access
3. You'll receive a `devid` and `key`

#### Step 2: Find Your Stop IDs
Use the search function to find stop IDs:

```python
from services.ptv_api import PTVService

ptv = PTVService(dev_id="YOUR_DEV_ID", api_key="YOUR_API_KEY")

# Search for your stop
stops = ptv.search_stops("Flinders Street", route_types=[0])  # 0=train, 1=tram

for stop in stops:
    print(f"{stop['stop_name']}: ID {stop['stop_id']}")
```

#### Step 3: Configure in settings.json
```json
{
  "ptv": {
    "devId": "YOUR_DEV_ID",
    "apiKey": "YOUR_API_KEY",
    "homeStopId": 1071,  // Your home stop ID
    "homeRouteType": 0,   // 0=train, 1=tram, 2=bus
    "workStopId": 1181,   // Your work stop ID
    "workRouteType": 0
  }
}
```

### Features
- Automatically determines morning (5am-12pm) vs evening (12pm-10pm) commute
- Shows next 3 departures with:
  - Minutes until departure
  - Destination
  - Route number
  - Platform (for trains)
- Updates every 30 seconds
- Color-coded urgency:
  - Red: Departing NOW
  - Orange: Departing in 5 minutes
  - White: Departing in 5+ minutes

### Display Modes

#### Compact Mode (Default)
Shows at bottom of clock screen:
- "Next train: 5 min"

#### Full Mode
Shows detailed departure list (toggle with config)

---

## Testing the Features

### Test Seasonal Themes
```bash
python src/main.py
# Look for season indicator in top-right corner
```

### Test Photo Frame
```bash
# Add some photos
cp ~/Pictures/*.jpg assets/photos/

# Run app and wait 60 seconds without interaction
python src/main.py
```

### Test Weekend Detection
```bash
# On a Saturday or Sunday, you'll see "Weekend" in top-left
python src/main.py
```

### Test Commute Planner
```bash
# After configuring PTV credentials
python src/main.py
# Look for departure info at bottom of screen
```

---

## Troubleshooting

### Photo Frame Not Working
- Check that photos exist in `assets/photos/`
- Verify idle timeout setting
- Ensure photos are valid image files

### PTV Not Showing
- Verify API credentials are correct
- Check stop IDs are valid
- Ensure you have internet connection
- Check console for error messages

### Holidays Not Detecting
- Holidays are hardcoded for 2024-2026
- Add more years in `src/services/holidays.py`

---

## Future Enhancements

Potential additions to these features:
- [ ] Custom photo frame transitions/effects
- [ ] API-based holiday fetching (auto-update)
- [ ] Bus route support for PTV
- [ ] Disruption/delay alerts for public transport
- [ ] Multiple commute route configurations
- [ ] Voice announcements for departures
