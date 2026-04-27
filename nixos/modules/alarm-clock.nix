{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.alarm-clock;
in {
  options.services.alarm-clock = {
    enable = mkEnableOption "Custom Alarm Clock Service";

    user = mkOption {
      type = types.str;
      default = "liv";
      description = "User to run the alarm clock application as";
    };

    autoStart = mkOption {
      type = types.bool;
      default = true;
      description = "Whether to start the alarm clock on boot";
    };
  };

  config = mkIf cfg.enable {
    systemd.services.alarm-clock = {
      description = "Custom Alarm Clock Application";
      wantedBy = mkIf cfg.autoStart [ "multi-user.target" ];
      after = [ "network.target" "display-manager.service" ];

      serviceConfig = {
        Type = "simple";
        User = cfg.user;
        ExecStart = "${pkgs.python311}/bin/python /home/${cfg.user}/alarm-clock/src/main.py";
        Restart = "on-failure";
        Environment = "DISPLAY=:0";
      };
    };
  };
}
