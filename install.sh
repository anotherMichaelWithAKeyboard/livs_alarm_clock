#!/bin/bash
#
# Installation script for Liv's Custom Alarm Clock on Raspberry Pi OS
#
# This script will:
# - Install system dependencies
# - Set up Python environment
# - Configure auto-login for the GUI
# - Set up the systemd service to auto-start the alarm clock
# - Configure timezone, audio, and touchscreen support
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$HOME/livs_alarm_clock"
SERVICE_NAME="alarm-clock.service"
USERNAME="${SUDO_USER:-$USER}"

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Liv's Custom Alarm Clock - Installation${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Check if running with sudo for system configuration
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run with sudo for system configuration${NC}"
    echo "Usage: sudo ./install.sh"
    exit 1
fi

echo -e "${YELLOW}Installing for user: $USERNAME${NC}"
echo ""

# Update package lists
echo -e "${GREEN}[1/8] Updating package lists...${NC}"
apt-get update

# Install system dependencies
echo -e "${GREEN}[2/8] Installing system dependencies...${NC}"
apt-get install -y \
    python3 \
    python3-pip \
    python3-pygame \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libportmidi-dev \
    pulseaudio \
    pavucontrol \
    xserver-xorg \
    lightdm \
    git \
    vim \
    openssh-server

# Install Python dependencies
echo -e "${GREEN}[3/8] Installing Python dependencies...${NC}"
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    sudo -u $USERNAME pip3 install --user -r "$PROJECT_DIR/requirements.txt"
else
    echo -e "${YELLOW}Warning: requirements.txt not found, skipping Python packages${NC}"
fi

# Set timezone to Melbourne
echo -e "${GREEN}[4/8] Setting timezone to Australia/Melbourne...${NC}"
timedatectl set-timezone Australia/Melbourne

# Configure audio
echo -e "${GREEN}[5/8] Configuring audio (PulseAudio)...${NC}"
# Add user to audio group
usermod -a -G audio $USERNAME

# Enable PulseAudio autospawn
sudo -u $USERNAME bash -c "mkdir -p ~/.config/pulse"
sudo -u $USERNAME bash -c "cat > ~/.config/pulse/client.conf << EOF
autospawn = yes
daemon-binary = /usr/bin/pulseaudio
EOF"

# Configure auto-login
echo -e "${GREEN}[6/8] Configuring auto-login for user $USERNAME...${NC}"
mkdir -p /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm.conf.d/50-autologin.conf << EOF
[Seat:*]
autologin-user=$USERNAME
autologin-user-timeout=0
EOF

# Install systemd service
echo -e "${GREEN}[7/8] Installing systemd service...${NC}"
if [ -f "$PROJECT_DIR/$SERVICE_NAME" ]; then
    # Update the service file with correct username
    sed "s/User=liv/User=$USERNAME/g; s/Group=liv/Group=$USERNAME/g; s|/home/liv/|/home/$USERNAME/|g" \
        "$PROJECT_DIR/$SERVICE_NAME" > /etc/systemd/system/$SERVICE_NAME

    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    echo -e "${GREEN}Systemd service installed and enabled${NC}"
else
    echo -e "${YELLOW}Warning: $SERVICE_NAME not found, skipping service installation${NC}"
fi

# Configure SSH
echo -e "${GREEN}[8/8] Configuring SSH...${NC}"
systemctl enable ssh
systemctl start ssh

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}  Installation Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo -e "Next steps:"
echo -e "  1. Configure your settings in: ${YELLOW}$PROJECT_DIR/config/settings.json${NC}"
echo -e "  2. Add alarm sounds to: ${YELLOW}$PROJECT_DIR/assets/sounds/${NC}"
echo -e "  3. Reboot to enable auto-login and auto-start: ${YELLOW}sudo reboot${NC}"
echo ""
echo -e "Useful commands:"
echo -e "  - Check service status: ${YELLOW}systemctl status $SERVICE_NAME${NC}"
echo -e "  - View service logs: ${YELLOW}journalctl -u $SERVICE_NAME -f${NC}"
echo -e "  - Start/stop service: ${YELLOW}systemctl start/stop $SERVICE_NAME${NC}"
echo -e "  - Disable auto-start: ${YELLOW}systemctl disable $SERVICE_NAME${NC}"
echo ""
