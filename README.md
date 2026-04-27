# Liv's Custom Alarm Clock

A custom alarm clock running on Raspberry Pi 5 with NixOS, featuring a touchscreen interface, weather forecasting, and customizable alarms.

## Project Structure

```
.
├── nixos/              # NixOS configuration
│   ├── modules/        # Custom NixOS modules
│   └── hardware/       # Hardware-specific configs
├── src/                # Application source code
│   ├── ui/            # User interface components
│   ├── services/      # Background services (alarm, weather API)
│   └── utils/         # Utility functions
├── assets/            # Static assets
│   ├── sounds/        # Alarm sound files
│   └── fonts/         # Custom fonts
├── config/            # Application configuration
└── tests/             # Test files
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
- Nix package manager with flakes enabled
- (For deployment) Raspberry Pi 5 with touchscreen

### Local Development
```bash
# Enter development shell
nix develop

# Run application locally (simulated)
python src/main.py

# Test individual components
python examples/test_split_flap.py  # Test split-flap display
python examples/test_pixel_border.py  # Test pixel border
```

### Deployment to Raspberry Pi
```bash
# Build NixOS configuration
nixos-rebuild build --flake .#alarm-clock

# Deploy to Raspberry Pi
nixos-rebuild switch --flake .#alarm-clock --target-host pi@alarm-clock.local
```

## TODO
- [ ] Purchase touchscreen
- [ ] Design 3D model case
- [ ] Print the case
