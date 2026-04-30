# Raspberry Pi OS Migration Guide

This project has been migrated from NixOS to Raspberry Pi OS for easier setup and broader compatibility.

## What Changed

### Removed (NixOS-specific)
- `flake.nix` - Nix flake configuration
- `shell.nix` - Nix development shell
- `nixos/` directory - NixOS system configuration files

**Note:** These files are kept in the repository for reference but are no longer actively used.

### Added (Raspberry Pi OS)
- `requirements.txt` - Python package dependencies
- `install.sh` - Automated installation script
- `alarm-clock.service` - Systemd service file for auto-start

### Updated Documentation
- `README.md` - Updated with Raspberry Pi OS instructions
- `QUICKSTART.md` - Simplified quick start without Nix
- `DEVELOPMENT.md` - Updated deployment instructions

## Quick Installation

On your Raspberry Pi 5 with Raspberry Pi OS:

```bash
# Clone the repository
cd ~
git clone <repository-url> livs_alarm_clock
cd livs_alarm_clock

# Run the automated installer
sudo ./install.sh

# Reboot
sudo reboot
```

The alarm clock will start automatically on boot!

## What the Installer Does

The `install.sh` script automates all setup:

1. **System Dependencies**
   - Python 3 and pip
   - pygame and SDL libraries
   - PulseAudio for sound
   - LightDM display manager
   - SSH server

2. **Python Packages**
   - pygame
   - requests
   - pytz

3. **System Configuration**
   - Sets timezone to Australia/Melbourne
   - Adds user to audio group
   - Configures PulseAudio

4. **Auto-Login Setup**
   - Configures LightDM to auto-login your user
   - Ensures GUI starts on boot

5. **Systemd Service**
   - Installs alarm-clock.service
   - Enables auto-start on boot
   - Sets up automatic restart on failure

## Manual Setup (Alternative)

If you prefer manual installation:

```bash
# Install system packages
sudo apt-get update
sudo apt-get install -y \
    python3 python3-pip python3-pygame \
    pulseaudio lightdm openssh-server

# Install Python dependencies
pip3 install -r requirements.txt

# Configure auto-login
sudo nano /etc/lightdm/lightdm.conf.d/50-autologin.conf
# Add:
# [Seat:*]
# autologin-user=YOUR_USERNAME
# autologin-user-timeout=0

# Install and start the service
sudo cp alarm-clock.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alarm-clock.service
sudo systemctl start alarm-clock.service
```

## Service Management

```bash
# Check if running
systemctl status alarm-clock.service

# View logs
journalctl -u alarm-clock.service -f

# Restart
sudo systemctl restart alarm-clock.service

# Stop
sudo systemctl stop alarm-clock.service

# Disable auto-start
sudo systemctl disable alarm-clock.service
```

## Advantages of Raspberry Pi OS

1. **Easier Setup** - Standard Debian packages, no Nix learning curve
2. **Better Hardware Support** - Official Raspberry Pi support
3. **Familiar Tools** - apt, systemd, standard Linux tools
4. **Community Support** - Larger user base for troubleshooting
5. **Direct Installation** - No need to build NixOS images

## NixOS Configuration (Archived)

The original NixOS configuration files remain in the `nixos/` directory for reference:
- `nixos/configuration.nix` - Main system config
- `nixos/modules/alarm-clock.nix` - Systemd service module
- `flake.nix` - Nix flake definition

These can be useful if you want to understand the original setup or potentially migrate back to NixOS in the future.

## Troubleshooting

### Service won't start
```bash
# Check logs for errors
journalctl -u alarm-clock.service -n 50

# Common issues:
# - Display not available: Make sure you're logged in to the GUI
# - Permission errors: Check user is in audio/video groups
# - Python errors: Verify all dependencies installed
```

### Display not showing
```bash
# Check X server is running
echo $DISPLAY  # Should show :0 or similar

# Try running manually
cd ~/livs_alarm_clock
python3 src/main.py
```

### Audio not working
```bash
# Check PulseAudio
pulseaudio --check
pulseaudio --start

# Test audio
speaker-test -t sine -f 1000 -l 1
```

## Migration Checklist

If migrating an existing NixOS installation:

- [ ] Back up your configuration (`config/` directory)
- [ ] Back up any custom alarm sounds
- [ ] Note your WiFi credentials
- [ ] Flash Raspberry Pi OS to SD card
- [ ] Clone repository on new system
- [ ] Run `install.sh`
- [ ] Restore your config files
- [ ] Copy alarm sounds to `assets/sounds/`
- [ ] Test the application
- [ ] Reboot and verify auto-start

## Support

For issues specific to Raspberry Pi OS setup, check:
- [Raspberry Pi OS Documentation](https://www.raspberrypi.com/documentation/computers/os.html)
- [systemd Documentation](https://www.freedesktop.org/software/systemd/man/)
- [Python pygame Documentation](https://www.pygame.org/docs/)
