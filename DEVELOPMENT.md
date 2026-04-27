# Development Guide

## Getting Started

### Using Nix Flakes (Recommended)
```bash
# Enable flakes in your nix configuration if not already enabled
# Add to ~/.config/nix/nix.conf or /etc/nix/nix.conf:
# experimental-features = nix-command flakes

# Enter development environment
nix develop

# Run the application
python src/main.py
```

### Using shell.nix (Legacy)
```bash
nix-shell
python src/main.py
```

### Without Nix
```bash
# Install dependencies
pip install pygame requests pytz

# Run the application
python src/main.py
```

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

### NixOS Configuration (`nixos/`)
- `configuration.nix` - Main NixOS configuration
- `hardware-configuration.nix` - Hardware-specific settings
- `modules/alarm-clock.nix` - Custom systemd service

## Testing on Your Laptop

The application is designed to run in a simulated environment. The default window size (800x480) matches typical small touchscreen displays.

### Controls
- Press `ESC` to exit the application
- Touch events will work if you have a touchscreen
- Mouse clicks simulate touch events

## Deploying to Raspberry Pi

### Prerequisites
1. Raspberry Pi 5 with SD card
2. NixOS installed on the Pi
3. Network connectivity to the Pi

### Build and Deploy
```bash
# Build the configuration
nix build .#nixosConfigurations.alarm-clock.config.system.build.toplevel

# Copy to Pi and switch (replace with your Pi's address)
nixos-rebuild switch --flake .#alarm-clock --target-host liv@alarm-clock.local --use-remote-sudo
```

### Initial Setup on Pi
1. Flash NixOS ARM image to SD card
2. Boot the Pi and get network access
3. Copy your SSH key: `ssh-copy-id liv@alarm-clock.local`
4. Deploy the configuration

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
