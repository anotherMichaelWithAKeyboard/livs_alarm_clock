{ config, pkgs, lib, ... }:

{
  # Import hardware configuration
  imports = [
    ./hardware-configuration.nix
    ./modules/alarm-clock.nix
  ];

  # Boot configuration for Raspberry Pi 5
  boot = {
    loader = {
      grub.enable = false;
      generic-extlinux-compatible.enable = true;
    };
  };

  # Networking
  networking = {
    hostName = "alarm-clock";
    wireless.enable = true;  # Or networkmanager if preferred
    firewall.enable = true;
  };

  # Enable SSH for remote management
  services.openssh = {
    enable = true;
    settings = {
      PermitRootLogin = "no";
      PasswordAuthentication = true;
    };
  };

  # Time zone (Melbourne)
  time.timeZone = "Australia/Melbourne";

  # User configuration
  users.users.liv = {
    isNormalUser = true;
    extraGroups = [ "wheel" "audio" "video" ];
    initialPassword = "changeme";
  };

  # System packages
  environment.systemPackages = with pkgs; [
    vim
    git
    python311
    python311Packages.pygame
    python311Packages.requests
    python311Packages.pytz
  ];

  # Enable X11 or Wayland for GUI
  services.xserver = {
    enable = true;
    displayManager = {
      autoLogin = {
        enable = true;
        user = "liv";
      };
      lightdm.enable = true;
    };
  };

  # Audio support
  sound.enable = true;
  hardware.pulseaudio.enable = true;

  # Touchscreen support
  services.xserver.libinput.enable = true;

  system.stateVersion = "24.05";
}
