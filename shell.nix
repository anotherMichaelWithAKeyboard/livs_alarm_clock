# Legacy shell.nix for non-flake users
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.pygame
    python311Packages.requests
    python311Packages.pytz
    python311Packages.pip
  ];

  shellHook = ''
    echo "Custom Alarm Clock Development Environment"
    echo "==========================================="
    echo "Python version: $(python --version)"
    echo ""
    echo "Run the application:"
    echo "  python src/main.py"
    echo ""
  '';
}
