{  pkgs, lib, config, ... }:
{

  cachix.enable = true;

  packages = [
    pkgs.socat
    pkgs.python312Packages.pygobject3
    pkgs.python312Packages.tkinter
    pkgs.gobject-introspection
    pkgs.gtk4
    pkgs.libadwaita
    pkgs.gst_all_1.gst-plugins-base
    pkgs.zlib
    pkgs.libGL
    pkgs.glib
    pkgs.xorg.libX11
  ];


  languages.python = {
    enable = true;
    version = "3.12";
    venv = {
        enable = true;
        requirements = ''
        pip
        colorama
        pytest
        numpy
        matplotlib
        tk
        PyQt6
        scipy
        '';
    };
  };

      enterShell = ''
    # Create a Python virtual environment for IDE compatibility
    if [ ! -L "$DEVENV_ROOT/venv" ]; then
        echo Creating a Python virtual environment for IDE compatibility
        ln -s "$DEVENV_STATE/venv/" "$DEVENV_ROOT/venv"
    fi
  '';

}

