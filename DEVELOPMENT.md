# Development Guide

## Getting Started

### Local Development (Linux/Mac/Windows)
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run the application
python3 src/main.py
```

The application will open in a window simulating the touchscreen display.

## Project Structure

### Application Code (`src/`)
- `main.py` - Entry point
- `ui/` - User interface components
  - `clock_display.py` - Main clock display
- `services/` - Background services
  - `alarm_manager.py` - Alarm scheduling and management
  - `weather_service.py` - Weather API integration
- `utils/` - Utility functions
  - `config_loader.py` - Configuration management

### Configuration (`config/`)
- `settings.json` - Application settings (display, dim mode, etc.)
- `alarms.json` - Saved alarms

### Deployment Files
- `requirements.txt` - Python package dependencies
- `install.sh` - Automated installation script for Raspberry Pi OS
- `alarm-clock.service` - Systemd service configuration

## Testing on Your Laptop

The application is designed to run in a simulated environment. The default window size (800x480) matches typical small touchscreen displays.

### Controls
- Press `ESC` to exit the application
- Touch events will work if you have a touchscreen
- Mouse clicks simulate touch events

## Deploying to Raspberry Pi

### Prerequisites
1. Raspberry Pi 5 with SD card
2. Raspberry Pi OS (64-bit recommended) installed
3. Network connectivity to the Pi
4. SSH access to the Pi

### Automated Deployment (Recommended)
```bash
# On your Raspberry Pi, clone the repository
cd ~
git clone <repository-url> livs_alarm_clock
cd livs_alarm_clock

# Run the installation script
sudo ./install.sh

# Reboot to enable auto-login and auto-start
sudo reboot
```

The installation script will:
- Install all system dependencies (Python, pygame, PulseAudio, etc.)
- Set up Python packages from requirements.txt
- Configure auto-login for the GUI
- Install and enable the systemd service
- Configure timezone to Australia/Melbourne
- Set up audio and touchscreen support

### Manual Deployment
```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-pygame pulseaudio lightdm openssh-server

# Install Python dependencies
pip3 install -r requirements.txt

# Configure auto-login (edit /etc/lightdm/lightdm.conf.d/50-autologin.conf)
# Add:
# [Seat:*]
# autologin-user=<your-username>
# autologin-user-timeout=0

# Install systemd service
sudo cp alarm-clock.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alarm-clock.service
sudo systemctl start alarm-clock.service
```

### Managing the Deployed Service
```bash
# Check service status
systemctl status alarm-clock.service

# View live logs
journalctl -u alarm-clock.service -f

# Restart the service
sudo systemctl restart alarm-clock.service

# Stop the service
sudo systemctl stop alarm-clock.service

# Disable auto-start
sudo systemctl disable alarm-clock.service
```

## Adding Features

### Adding a New Alarm Sound
1. Add `.mp3`, `.wav`, or `.ogg` file to `assets/sounds/`
2. The file will be available in the alarm sound selection menu

### Integrating Weather API
1. Get API key from BOM or WillyWeather
2. Update `config/settings.json` with your API key
3. Implement the API calls in `src/services/weather_service.py`

### Customizing the Display
Modify `src/ui/clock_display.py`:
- Colors are defined in `__init__`
- Layout is in `draw_clock` method
- Add new UI elements by creating new methods

## TODO Features to Implement
- [ ] Flip animation for time display
- [ ] Touch-based alarm setting menu
- [ ] Weather forecast display
- [ ] "Can ride" indicator
- [ ] Settings menu
- [ ] Dim mode scheduler
- [ ] Audio playback for alarms
- [ ] Multiple alarm support
