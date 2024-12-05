
# repeat for for nix package "figlet"
# if [ -f "$HOME/.nix-profile/bin/nix-env" ]; then

#   echo "----------------------------- installing nix ----------------------------"
#   ~/.nix-profile/bin/nix-env -iA nixpkgs.cowsay || true
#   ~/.nix-profile/bin/nix-env -iA nixpkgs.lolcat || true
#   ~/.nix-profile/bin/nix-env -iA nixpkgs.boxes || true
#   ~/.nix-profile/bin/nix-env -iA nixpkgs.figlet || true

# else

  # check if path "/usr/games/cowsay" exists, if not install boxes:
if [ ! -f "/usr/games/cowsay" ]; then
  echo "----------------------------- installing boxes ----------------------------"
  sudo nala install cowsay -y || true  # for ascii banners. boxes -l for list of boxes.
fi

# repeat for "/usr/games/lolcat"
if [ ! -f "/usr/games/lolcat" ]; then
  echo "----------------------------- installing lolcat ----------------------------"
  sudo nala install lolcat -y || true  # for coloring text in terminal.
fi

# repeat for "/usr/bin/boxes"
if [ ! -f "/usr/bin/boxes" ]; then
  echo "----------------------------- installing cowsay ----------------------------"
  sudo nala install boxes -y || true  # animals saying things. Different figures with -f. Full list: cowsay -l
fi

# repeat for "/usr/bin/figlet
if [ ! -f "/usr/bin/figlet" ]; then
  echo "----------------------------- installing figlet ----------------------------"
  sudo nala install figlet -y || true  # large ascii text. See: showfigfonts for full list of fonts. use -f to change font.
fi

# fi
