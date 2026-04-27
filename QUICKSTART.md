# Quick Start Guide

## Test the Application Locally

### Option 1: Using Nix (Recommended)
```bash
# Enter development environment
nix develop

# Run the application
python src/main.py
```

### Option 2: Using Python directly
```bash
# Install dependencies
pip install pygame requests pytz

# Run the application
python src/main.py
```

You should see a window with a digital clock showing Melbourne time. Press ESC to exit.

## Next Steps

1. **Test the basic clock display**
   - Run `python src/main.py`
   - Verify the time shows correctly in 12-hour format
   - Check that the date displays properly

2. **Add custom alarm sounds**
   - Place `.mp3` or `.wav` files in `assets/sounds/`
   - See `assets/sounds/README.md` for more info

3. **Configure settings**
   - Edit `config/settings.json` to adjust display and dim mode settings
   - Add weather API key when ready

4. **Prepare for Raspberry Pi deployment**
   - Review `nixos/configuration.nix`
   - Adjust hardware settings as needed
   - See `DEVELOPMENT.md` for deployment instructions

## Current Status

### Working Features
- ✅ Basic digital clock display
- ✅ Melbourne timezone support
- ✅ Configuration system
- ✅ Alarm manager (backend)
- ✅ Weather service structure

### To Be Implemented
- ⏳ Flip animation for clock
- ⏳ Touch-based UI menus
- ⏳ Alarm setting interface
- ⏳ Weather forecast display
- ⏳ "Can ride" cycling indicator
- ⏳ Settings menu UI
- ⏳ Dim mode implementation
- ⏳ Audio alarm playback

## Troubleshooting

### "ModuleNotFoundError: No module named 'pygame'"
Install pygame: `pip install pygame` or use `nix develop`

### Display is too small/large
Adjust `width` and `height` in `config/settings.json`

### Wrong timezone
Change `timezone` in `config/settings.json` to your preferred timezone

## Resources
- [NixOS Manual](https://nixos.org/manual/nixos/stable/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Raspberry Pi 5 Specs](https://www.raspberrypi.com/products/raspberry-pi-5/)
