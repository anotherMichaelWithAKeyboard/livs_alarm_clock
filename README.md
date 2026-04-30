# Liv's Custom Alarm Clock

A custom alarm clock running on Raspberry Pi 5 with Raspberry Pi OS, featuring a touchscreen interface, weather forecasting, and customizable alarms.

## Project Structure

```
.
├── src/                # Application source code
│   ├── ui/            # User interface components
│   ├── services/      # Background services (alarm, weather API)
│   └── utils/         # Utility functions
├── assets/            # Static assets
│   ├── sounds/        # Alarm sound files
│   └── fonts/         # Custom fonts
├── config/            # Application configuration
├── tests/             # Test files
├── requirements.txt   # Python dependencies
├── install.sh         # Installation script for Raspberry Pi OS
└── alarm-clock.service # Systemd service file
```

## Features

### Core Features
- **Digital Clock Display** - 12-hour format synced to Melbourne time
- **Alarm Management** - Set alarms with custom sounds and sleep duration preview
- **Weather Forecast** - BOM/WillyWeather integration with "can ride" cycling conditions
- **Settings** - Dim mode scheduling and auto-dim options
- **SSH Access** - Remote configuration and updates

### New Features ✨
- **Seasonal Themes** - Automatic color scheme changes based on Australian seasons
- **Photo Frame Mode** - Displays your photos after idle timeout
- **Weekend/Holiday Detection** - No accidental 6am wake-ups on Saturday or public holidays
- **Commute Planner** - Real-time train/tram departure times (PTV API)

### Visual Design 🎨
- **Split-Flap Display** - Retro airport-style with digital 7-segment LED digits
- **Pixel Art Border** - Seasonal vines and mushroom people
- **Rare Mushroom System** - Collectible mushroom variants (Common → Legendary!)
  - Uncommon (20%): Tall Mushroom 🌟
  - Rare (10%): Crowned Mushroom ⭐⭐
  - Very Rare (5%): Spotted Giant ⭐⭐⭐
  - **LEGENDARY (1%): Mushroom Queen** 👑✨

See [FEATURES.md](FEATURES.md), [VISUAL_FEATURES.md](VISUAL_FEATURES.md), and [RARE_MUSHROOMS.md](RARE_MUSHROOMS.md) for details.

## Development

### Prerequisites
- Python 3.x
- Raspberry Pi 5 with touchscreen (for deployment)
- Raspberry Pi OS (64-bit recommended)

### Local Development
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run application locally
python3 src/main.py

# Test individual components
python3 examples/test_split_flap.py  # Test split-flap display
python3 examples/test_pixel_border.py  # Test pixel border
```

### Deployment to Raspberry Pi

#### Option 1: Automated Installation (Recommended)
```bash
# Clone the repository on your Raspberry Pi
cd ~
git clone <repository-url> livs_alarm_clock
cd livs_alarm_clock

# Run the installation script
sudo ./install.sh

# Reboot to enable auto-login and auto-start
sudo reboot
```

#### Option 2: Manual Installation
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip python3-pygame pulseaudio lightdm

# Install Python dependencies
pip3 install -r requirements.txt

# Install systemd service
sudo cp alarm-clock.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alarm-clock.service
sudo systemctl start alarm-clock.service
```

### Managing the Service
```bash
# Check service status
systemctl status alarm-clock.service

# View logs
journalctl -u alarm-clock.service -f

# Restart the service
sudo systemctl restart alarm-clock.service

# Stop the service
sudo systemctl stop alarm-clock.service
```

## TODO
- [ ] Purchase touchscreen
- [ ] Design 3D model case
- [ ] Print the case
