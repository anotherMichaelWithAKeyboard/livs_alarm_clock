# Quick Start Guide

## Test the Application Locally

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the application
python3 src/main.py
```

You should see a window with a digital clock showing Melbourne time. Press ESC to exit.

## Next Steps

1. **Test the basic clock display**
   - Run `python3 src/main.py`
   - Verify the time shows correctly in 12-hour format
   - Check that the date displays properly

2. **Add custom alarm sounds**
   - Place `.mp3` or `.wav` files in `assets/sounds/`
   - See `assets/sounds/README.md` for more info

3. **Configure settings**
   - Edit `config/settings.json` to adjust display and dim mode settings
   - Add weather API key when ready

4. **Deploy to Raspberry Pi**
   - Copy project to your Raspberry Pi 5
   - Run the installation script: `sudo ./install.sh`
   - See README.md for detailed deployment instructions

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
Install dependencies: `pip3 install -r requirements.txt`

### Display is too small/large
Adjust `width` and `height` in `config/settings.json`

### Wrong timezone
Change `timezone` in `config/settings.json` to your preferred timezone

### Service not starting after installation
Check service logs: `journalctl -u alarm-clock.service -f`

## Resources
- [Raspberry Pi OS Documentation](https://www.raspberrypi.com/documentation/computers/os.html)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Raspberry Pi 5 Specs](https://www.raspberrypi.com/products/raspberry-pi-5/)
