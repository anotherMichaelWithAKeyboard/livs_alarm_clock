{
  description = "Custom Alarm Clock for Raspberry Pi 5";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    nixos-hardware.url = "github:NixOS/nixos-hardware/master";
  };

  outputs = { self, nixpkgs, nixos-hardware }: {
    # NixOS configuration for Raspberry Pi 5
    nixosConfigurations.alarm-clock = nixpkgs.lib.nixosSystem {
      system = "aarch64-linux";
      modules = [
        nixos-hardware.nixosModules.raspberry-pi-5
        ./nixos/configuration.nix
      ];
    };

    # Development shell
    devShells.x86_64-linux.default =
      let pkgs = nixpkgs.legacyPackages.x86_64-linux;
      in pkgs.mkShell {
        buildInputs = with pkgs; [
          python311
          python311Packages.pygame
          python311Packages.requests
          python311Packages.pytz
        ];
      };

    # Development shell for aarch64 (if developing on ARM)
    devShells.aarch64-linux.default =
      let pkgs = nixpkgs.legacyPackages.aarch64-linux;
      in pkgs.mkShell {
        buildInputs = with pkgs; [
          python311
          python311Packages.pygame
          python311Packages.requests
          python311Packages.pytz
        ];
      };
  };
}
